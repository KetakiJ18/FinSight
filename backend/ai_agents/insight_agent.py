from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate


class InsightGenerationAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2:1b",
            temperature=0.2
        )

    def generate_insights(self, kpi_results: str):
        prompt = PromptTemplate(
            input_variables=["kpi_results"],
            template="""
You are a Chief Financial Officer summarizing financial performance.
Provide an executive summary of these key performance indicators:

{kpi_results}
"""
        )

        chain = prompt | self.llm
        return chain.invoke({"kpi_results": kpi_results})