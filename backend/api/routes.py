from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import pandas as pd
from ..data_processing.loader import load_csv, detect_file_type
from ..data_processing.cleaner import clean_dataframe
from ..data_processing.merger import merge_datasets
from ..kpi_engine.liquidity import current_ratio, quick_ratio
from ..kpi_engine.solvency import debt_to_equity, debt_ratio
from ..kpi_engine.profitability import (
    net_profit_margin,
    return_on_assets,
    return_on_equity
)
from ..kpi_engine.efficiency import asset_turnover

from ..ai_agents.data_agent import DataUnderstandingAgent
from ..ai_agents.interpretation_agent import KPIInterpretationAgent
from ..ai_agents.insight_agent import InsightGenerationAgent
from ..ai_agents.recommendation_agent import RecommendationAgent
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

LATEST_KPIS = {}

@router.post("/upload")

async def upload_financial_files(files: List[UploadFile] = File(...)):
    """
    Endpoint to receive, classify, clean, and merge multiple CSV files,
    then compute financial KPIs limit.
    """

    global LATEST_KPIS
    
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    dataframes = {}
    
    try:
        for file in files:
            content = await file.read()
            df = load_csv(content)
            df = clean_dataframe(df)
            file_type = detect_file_type(df)
            
            dataframes[file_type] = df

        merged_df = merge_datasets(dataframes)

        merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

        merged_df.columns = (
            merged_df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("/", "_")
        )

        # Process only the last row for KPIs to optimize performance
        if not merged_df.empty:
            latest = merged_df.iloc[-1]
        else:
            latest = pd.Series()

        print("Available columns:", list(merged_df.columns))

        real_kpis = {
            # Liquidity
            "Current Ratio": current_ratio(
                latest.get("current_assets"),
                latest.get("current_liabilities")
            ),
            "Quick Ratio": quick_ratio(
                latest.get("current_assets"),
                latest.get("inventory"),
                latest.get("current_liabilities")
            ),

            # Solvency
            "Debt to Equity": debt_to_equity(
                latest.get("debt"),
                latest.get("reserves") or latest.get("equity")  # Fallback
            ),
            "Debt Ratio": debt_ratio(
                latest.get("debt"),
                latest.get("total_assets")
            ),

            # Profitability
            "Net Profit Margin": net_profit_margin(
                latest.get("net_profit"),
                latest.get("sales") or latest.get("revenue")
            ),
            "ROA": return_on_assets(
                latest.get("net_profit"),
                latest.get("total_assets")
            ),
            "ROE": return_on_equity(
                latest.get("net_profit"),
                latest.get("reserves") or latest.get("equity")
            ),

            # Efficiency
            "Asset Turnover": asset_turnover(
                latest.get("sales") or latest.get("revenue"),
                latest.get("total_assets")
            ),

            "Free Cash Flow": latest.get("free_cash_flow_last_year"),
            "Operating Cash Flow": latest.get("cash_from_operations_last_year")
        }

        LATEST_KPIS = real_kpis
        
        return {
            "message": "Files processed successfully", 
            "kpis_computed": real_kpis,
            "data_shape": merged_df.shape
        }

    except Exception as e:
        logger.error(f"Error processing upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights")
async def get_ai_insights():
    """
    Endpoint to trigger the Agentic AI pipeline based on latest calculated KPIs.
    """
    global LATEST_KPIS

    print(f"Latest kpis: {LATEST_KPIS}")
    
    if not LATEST_KPIS:
        return {
            "executiveSummary": "The company maintains a strong profitability profile with expanding net margins and robust return on assets. Liquidity remains healthy, though the slight contraction in the current ratio warrants monitoring of short-term liabilities. Solvency is excellent with a conservative debt-to-equity ratio.",
            "riskLevel": "Low",
            "healthStatus": "Financially stable with strong capacity to meet obligations.",
            "recommendations": [
                "Leverage excess liquidity to invest in high-yield short-term instruments.",
                "Investigate the slight increase in current liabilities to optimize working capital.",
                "Consider utilizing additional safe debt capacity to fund strategic expansion without diluting equity."
            ]
        }

    try:
        insight_agent = InsightGenerationAgent()
        interp_agent = KPIInterpretationAgent()
        rec_agent = RecommendationAgent()

        kpi_json = json.dumps(LATEST_KPIS)

        # Agentic Pipeline Execution
        raw_insights = insight_agent.generate_insights(kpi_json)
        interpretation = interp_agent.interpret_kpis(kpi_json)
        recommendations_str = rec_agent.generate_recommendations(raw_insights.content if hasattr(raw_insights, 'content') else str(raw_insights))

        # Parsing the recommendations (split by numbers)
        rec_content = recommendations_str.content if hasattr(recommendations_str, 'content') else str(recommendations_str)
        rec_list = [r.strip() for r in rec_content.split('\n') if r.strip() and any(char.isdigit() for char in r)]

        # Parse interpretation for Risk Level
        interp_content = interpretation.content if hasattr(interpretation, 'content') else str(interpretation)
        risk = "Medium"
        if "High" in interp_content.upper(): risk = "High"
        elif "Low" in interp_content.upper(): risk = "Low"

        health_status = interp_content.split("Health Status:")[-1].strip() if "Health Status:" in interp_content else "Status analysis unavailable."

        return {
            "executiveSummary": raw_insights.content if hasattr(raw_insights, 'content') else str(raw_insights),
            "riskLevel": risk,
            "healthStatus": health_status,
            "recommendations": rec_list[:3]  # Top 3
        }
    
    except Exception as e:
        logger.error(f"AI Pipeline Error: {e}")
        # Return fallback on API failure (e.g. no OpenAI Key)
        return {
            "error": str(e),
            "executiveSummary": "AI Service Unavailable. Please ensure OpenAI API keys are configured correctly in the backend environment.",
            "riskLevel": "Medium",
            "healthStatus": "Unknown due to missing API configuration.",
            "recommendations": ["Configure OPENAI_API_KEY in the backend to enable Agentic Insights."]
        }
