from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from state import AgentState
from nodes import author_node, collector_node, assessor_node, hint_node

def route_after_assessor(state: AgentState):
    latest_score = state["scores"][-1]
    if latest_score >= 0.8:
        return "END"
    else:
        return "hint"

graph = StateGraph(AgentState)

graph.add_node("author", author_node)
graph.add_node("collector", collector_node)
graph.add_node("assessor", assessor_node)
graph.add_node("hint", hint_node)

graph.set_entry_point("author")
graph.add_edge("author", "collector")
graph.add_edge("collector", "assessor")
graph.add_edge("hint", "collector")

graph.add_conditional_edges("assessor", route_after_assessor, {
    "END": END,
    "hint": "hint"
})

with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
    app = graph.compile(checkpointer=checkpointer)
    app.invoke(
        {
            "topic": "animal trivia",
            "draft": "",
            "submissions": [],
            "scores": [],
            "hints_given": []
        },
        config={"configurable": {"thread_id": "student_123"}}
    )