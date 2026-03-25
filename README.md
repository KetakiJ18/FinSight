# FinSight AI: Intelligent Financial KPI & AI Analysis Platform

FinSight AI transforms raw financial statement data into clear, actionable business intelligence. It acts as an **AI Financial Analyst Assistant** that processes financial CSVs (P&L, Balance Sheets, Cash Flow), calculates key financial metrics, and generates natural-language insights via an Agentic AI pipeline.

## 🚀 Features

- **Automated KPI Engine**: Calculates Profitability (Net Profit Margin, ROA, ROE), Liquidity (Current/Quick Ratios), Solvency (Debt-to-Equity), and Efficiency (Asset Turnover).
- **Agentic AI Pipeline**: Langchain orchestrated agents interpret KPIs, determine financial health, classify risk levels, and output actionable business recommendations.
- **Modern Fintech Dashboard**: Built with React, Vite, and Tailwind CSS. Features drag-and-drop file upload, KPI indicator cards, and a dynamic AI insight panel.
- **Future-Ready Architecture**: Designed for modularity to support scaling toward automated workflows (e.g., n8n scheduling or email reporting).

---

## 🏗️ Project Architecture

```
finsight-ai/
│
├── frontend/                 # React UI Dashboard
│   ├── src/components/
│   ├── src/services/         # Axios API connections
│   └── src/utils/
│
├── backend/                  # FastAPI Application
│   ├── data_processing/      # CSV Loaders, Cleaners, and Mergers
│   ├── kpi_engine/           # Calculation routines for core metrics
│   ├── ai_agents/            # LangChain AI workflow (Insight, Recs, Data)
│   └── api/                  # FastAPI endpoints (/upload, /insights)
│
└── dataset/                  # Sample CSVs provided
```

---

## 🛠️ Installation Guide

### Prerequisites
- Node.js (v18+)
- Python 3.9+
- An OpenAI API Key

### Backend Setup (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your Environment Variable:
   ```bash
   export OPENAI_API_KEY="your-sk-key" 
   # On Windows: set OPENAI_API_KEY="your-sk-key"
   ```
5. Start the API Server:
   ```bash
   uvicorn main:app --reload
   ```
   *The backend will run on http://localhost:8000*

### Frontend Setup (React + Vite)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```
   *The frontend will run on http://localhost:5173*

---

## 📖 Usage Instructions

1. Open the UI at `http://localhost:5173`.
2. Locate the "Upload Financial Statements" panel on the homepage.
3. Drag and drop your `.csv` files (e.g., `annual_PL1.csv`, `balance_sheet.csv`) from the `./dataset` folder into the upload zone.
4. The system automatically reads, cleans, and merges the data inside the backend.
5. Watch the dashboard populate with real-time KPI value cards showing metrics like Net Profit Margin and Debt-to-Equity.
6. Below the KPI cards, the **AI Insights Panel** will generate an Executive Summary, a Health/Risk Level indicator, and actionable recommendations utilizing the LLM pipeline.

---

## 🤖 AI Pipeline Explanation

The intelligence layer utilizes LangChain to orchestrate a series of single-purpose AI agents:
- **Data Understanding Agent**: Translates the raw numeric Pandas dataframe shapes into narrative strings.
- **KPI Interpretation Agent**: Analyzes the calculated ratios (e.g. Current Ratio) against industry baselines to assign a Risk Level (Low/Medium/High).
- **Insight Generation Agent**: Formulates an Executive Summary simulating a CFO's analysis.
- **Recommendation Agent**: Consumes the insights and returns numbered, actionable business strategies.
