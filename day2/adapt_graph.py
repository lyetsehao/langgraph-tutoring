from langgraph.graph import StateGraph, END
from state import AgentState

from llm import llm

def adapt_node(state: AgentState):
    topic = state["topic"]
    scores = state["scores"]
    hints = state["hints_given"]
    submissions = state["submissions"]
    attempts = len(submissions)
    hints_used = len(hints)
    response = llm.invoke(
        f"A student just completed a {topic} trivia question. "
        f"They took {attempts} attempts and used {hints_used} hints. "
        f"Their scores per attempt were: {scores}. "
        f"Based on this performance, should the next question be easier, same, or harder? "
        f"Return only one word: 'easier', 'same', or 'harder'."
    )
    recommendation = response.content.strip().lower()
    print(f"\n--- Difficulty recommendation: {recommendation} ---\n")
    return {}

graph = StateGraph(AgentState)
graph.add_node("adapt", adapt_node)
graph.set_entry_point("adapt")
graph.add_edge("adapt", END)

adapt_app = graph.compile()