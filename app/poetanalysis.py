# poet_analysis_agent_v2.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.tools.tavily_search import TavilySearchResults

load_dotenv()

class PoetAnalysisAgent:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=self.google_api_key
        )

        self.search_tool = TavilySearchResults(api_key=self.tavily_api_key)

        self.summary_prompt = PromptTemplate(
            input_variables=["name", "context"],
            template="""
You are a literary analysis AI.

Based on the following context, write a detailed paragraph summarizing the poetic style and themes of "{name}". 
Include information on tone, grammar, themes, language, and historical influence.

Context:
{context}

Summary:
"""
        )

        self.refinement_prompt = PromptTemplate(
            input_variables=["summary"],
            template="""
You are a summary refinement expert.

Improve the following summary to make it more structured, poetic, and insightful. Make sure it's fluent, literary in tone, and free from errors.

Original Summary:
{summary}

Refined Summary:
"""
        )

    def search_poet_context(self, poet_name: str, max_results: int = 5) -> str:
        print(f"🔍 Searching for: {poet_name}")
        results = self.search_tool.run(f"{poet_name} poet writing style analysis")
        return "\n".join([r['content'] for r in results[:max_results]])

    def generate_summary(self, poet_name: str, context: str) -> str:
        prompt = self.summary_prompt.format(name=poet_name, context=context)
        return self.llm.invoke(prompt)

    def refine_summary(self, raw_summary: str) -> str:
        prompt = self.refinement_prompt.format(summary=raw_summary)
        return self.llm.invoke(prompt)

# ✅ Example Usage
if __name__ == "__main__":
    agent = PoetAnalysisAgent()
    poet_name = "Sylvia Plath"

    context = agent.search_poet_context(poet_name)
    raw_summary = agent.generate_summary(poet_name, context)
    refined_summary = agent.refine_summary(raw_summary)

    print("\n🧾 Final Refined Summary:\n")
    print(refined_summary.content)
