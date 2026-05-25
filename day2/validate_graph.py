from langgraph.graph import StateGraph, END
from state import AgentState
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def validate_node(state: AgentState):
    problem = state["problem"]
    answer = state["answer"]
    response = llm.invoke(
        f"Is this answer correct for this question? "
        f"Question: {problem} "
        f"Answer: {answer} "
        f"Return only 'valid' or 'invalid', nothing else."
    )
    result = response.content.strip().lower()
    print(f"\n--- Validation: {result} ---\n")
    return {"problem": problem, "answer": answer}

graph = StateGraph(AgentState)
graph.add_node("validate", validate_node)
graph.set_entry_point("validate")
graph.add_edge("validate", END)

validate_app = graph.compile()