from langgraph.graph import StateGraph, END
from state import AgentState

from llm import llm

def collector_node(state: AgentState):
    print("\n--- Problem ---")
    print(state["problem"])
    print("---------------\n")
    if state["hints_given"]:
        print("--- Hints so far ---")
        for i, hint in enumerate(state["hints_given"], 1):
            print(f"{i}. {hint}")
        print("--------------------\n")
    submission = input("Your answer: ")
    return {"submissions": [submission]}

def assessor_node(state: AgentState):
    problem = state["problem"]
    answer = state["answer"]
    latest_submission = state["submissions"][-1]
    response = llm.invoke(
        f"Question: {problem} "
        f"Correct answer: {answer} "
        f"Student answer: {latest_submission} "
        f"Is the student's answer correct? Award 1 if correct or close enough, 0 if wrong. Return only 0 or 1, nothing else."
    )
    score = float(response.content.strip())
    print(f"\n--- Score: {score} ---\n")
    return {"scores": [score]}

graph = StateGraph(AgentState)
graph.add_node("collector", collector_node)
graph.add_node("assessor", assessor_node)
graph.set_entry_point("collector")
graph.add_edge("collector", "assessor")
graph.add_edge("assessor", END)

assess_app = graph.compile()
