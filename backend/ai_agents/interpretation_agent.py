from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate


class KPIInterpretationAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2:1b",
            temperature=0.1
        )

    def interpret_kpis(self, raw_kpis: str):
        prompt = PromptTemplate(
            input_variables=["raw_kpis"],
            template="""
You are a financial risk analyst.
Interpret the following raw KPIs and determine financial health status.
Classify risk levels as Low, Medium, or High.

{raw_kpis}
"""
        )

        chain = prompt | self.llm
        return chain.invoke({"raw_kpis": raw_kpis})