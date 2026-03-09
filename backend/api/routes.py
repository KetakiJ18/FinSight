from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import pandas as pd
from ..data_processing.loader import load_csv, detect_file_type
from ..data_processing.cleaner import clean_dataframe
from ..data_processing.merger import merge_datasets
from ..kpi_engine import profitability, liquidity, solvency, efficiency
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

        merged_df.columns = merged_df.columns.str.strip().str.lower()

        latest = merged_df.iloc[-1]

        print(latest[[
            "current_ratio",
            "interest_coverage_ratio",
            "price_to_sales",
            "price_to_free_cash_flow",
            "evebitda"
        ]])

        current_ratio = float(latest.get("current_ratio", 0))
        interest_coverage = float(latest.get("interest_coverage_ratio", 0))
        price_to_sales = float(latest.get("price_to_sales", 0))
        price_to_fcf = float(latest.get("price_to_free_cash_flow", 0))
        ev_ebitda = float(latest.get("evebitda", 0))

        real_kpis = {
            "Current Ratio": current_ratio,
            "Interest Coverage Ratio": interest_coverage,
            "Price to Sales": price_to_sales,
            "Price to Free Cash Flow": price_to_fcf,
            "EV/EBITDA": ev_ebitda
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
        recommendations_str = rec_agent.generate_recommendations(raw_insights.content if hasattr(raw_insights, 'content') else raw_insights)

        # Parsing the recommendations (naively splitting by newline for demo)
        rec_content = recommendations_str.content if hasattr(recommendations_str, 'content') else recommendations_str
        rec_list = [r.strip("- ") for r in rec_content.split("\n") if r.strip()]

        # Parse interpretation for Risk Level (naive extraction)
        interp_content = interpretation.content if hasattr(interpretation, 'content') else interpretation
        risk = "Medium"
        if "High" in interp_content: risk = "High"
        elif "Low" in interp_content: risk = "Low"

        return {
            "executiveSummary": raw_insights.content if hasattr(raw_insights, 'content') else raw_insights,
            "riskLevel": risk,
            "healthStatus": interp_content[:150] + "...", # Truncated summary
            "recommendations": rec_list[:3] # Top 3
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
