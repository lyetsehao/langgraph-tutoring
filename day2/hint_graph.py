from langgraph.graph import StateGraph, END
from state import AgentState
from llm import llm

hint_cache = {}

def get_cache_key(problem: str, submission: str) -> str:
    return f"{problem}:{submission}"

def hint_node(state: AgentState):
    problem = state["problem"]
    answer = state["answer"]
    latest_submission = state["submissions"][-1]
    previous_hints = state["hints_given"]

    cache_key = get_cache_key(problem, latest_submission)

    # Check cache first
    if cache_key in hint_cache:
        print(f"\n--- Hint (from cache): {hint_cache[cache_key]} ---\n")
        return {"hints_given": [hint_cache[cache_key]]}

    max_attempts = 3
    for attempt in range(max_attempts):
        response = llm.invoke(
            f"A student is answering this question: {problem} "
            f"The correct answer is: {answer} "
            f"The student answered: {latest_submission} "
            f"Previous hints given: {previous_hints} "
            f"Give a helpful hint that guides them towards the answer without revealing it directly. "
            f"Do not repeat previous hints."
        )
        hint = response.content.strip()

        # Anti-spoiler check
        spoiler_check = llm.invoke(
            f"Question: {problem} "
            f"Answer: {answer} "
            f"Hint: {hint} "
            f"On a scale of 1-10, how much does this hint reveal the answer? "
            f"1 = no spoiler at all, 10 = gives the answer away completely. "
            f"Return only a number, nothing else."
        )

        try:
            spoiler_score = float(spoiler_check.content.strip())
        except:
            spoiler_score = 5

        print(f"\n--- Hint spoiler score: {spoiler_score} ---\n")

        if spoiler_score <= 6:
            hint_cache[cache_key] = hint
            print(f"\n--- Hint: {hint} ---\n")
            return {"hints_given": [hint]}
        else:
            print(f"\n--- Hint too revealing, regenerating... ---\n")

    hint_cache[cache_key] = hint
    print(f"\n--- Hint: {hint} ---\n")
    return {"hints_given": [hint]}

graph = StateGraph(AgentState)
graph.add_node("hint", hint_node)
graph.set_entry_point("hint")
graph.add_edge("hint", END)

hint_app = graph.compile()