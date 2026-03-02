from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate

class DataUnderstandingAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2:1b",
            temperature=0
        )

    def analyze_data(self, data_summary: str):
        prompt = PromptTemplate(
            input_variables=["data_summary"],
            template="""
You are an expert financial data analyst.
Review this summary of financial data and provide key observations:

{data_summary}
"""
        )

        chain = prompt | self.llm
        return chain.invoke({"data_summary": data_summary})