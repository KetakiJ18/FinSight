from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate


class RecommendationAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2:1b",
            temperature=0.7
        )

    def generate_recommendations(self, insights: str):
        prompt = PromptTemplate(
            input_variables=["insights"],
            template="""You are a financial advisor.

Based on these insights, provide exactly 3 actionable business recommendations.
Keep them short, practical, and clear. Number them 1-3.

Financial insights:
{insights}

Recommendations:"""
        )

        try:
            chain = prompt | self.llm
            response = chain.invoke({"insights": insights})
            return response
        except Exception as e:
            return f"AI Recommendations Failed: {str(e)}. Default: 1. Review financial statements. 2. Consult financial advisor. 3. Monitor key metrics."