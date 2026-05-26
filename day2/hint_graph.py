from langgraph.graph import StateGraph, END
from state import AgentState

from llm import llm

def hint_node(state: AgentState):
    problem = state["problem"]
    answer = state["answer"]
    latest_submission = state["submissions"][-1]
    previous_hints = state["hints_given"]
    response = llm.invoke(
        f"A student is answering this question: {problem} "
        f"The correct answer is: {answer} "
        f"The student answered: {latest_submission} "
        f"Previous hints given: {previous_hints} "
        f"Give a helpful hint that guides them towards the answer without revealing it directly. "
        f"Do not repeat previous hints."
    )
    hint = response.content.strip()
    print(f"\n--- Hint: {hint} ---\n")
    return {"hints_given": [hint]}

graph = StateGraph(AgentState)
graph.add_node("hint", hint_node)
graph.set_entry_point("hint")
graph.add_edge("hint", END)

hint_app = graph.compile()