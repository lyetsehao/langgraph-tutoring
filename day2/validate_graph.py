from langgraph.graph import StateGraph, END
from state import AgentState
from llm import llm
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def validate_node(state: AgentState):
    problem = state["problem"]
    answer = state["answer"]
    
    # Search the web to verify the fact
    search_result = tavily.search(f"{problem} {answer}")
    context = " ".join([r["content"] for r in search_result["results"][:3]])
    
    # Ask LLM to verify using real search results
    response = llm.invoke(
        f"Based on these web search results: {context} "
        f"Is this question and answer factually correct? "
        f"Question: {problem} "
        f"Answer: {answer} "
        f"Return only 'valid' or 'invalid', nothing else."
    )
    result = response.content.strip().lower()
    print(f"\n--- Validation: {result} ---\n")
    
    if result == "invalid":
        print("--- Question failed validation, regenerating... ---\n")
        return {"problem": "", "answer": ""}
    
    return {"problem": problem, "answer": answer}

graph = StateGraph(AgentState)
graph.add_node("validate", validate_node)
graph.set_entry_point("validate")
graph.add_edge("validate", END)

validate_app = graph.compile()