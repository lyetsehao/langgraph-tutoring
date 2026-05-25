from state import AgentState
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key="ANTHROPIC_API_KEY"
)

def author_node(state: AgentState):
    topic = state["topic"]
    draft = llm.invoke(f"Ask me a single trivia question about {topic}. Do not reveal or hint at the answer in the question. Only ask the question, nothing else.")
    return {"draft": draft.content}

def collector_node(state: AgentState):
    print("\n--- Problem ---")
    print(state["draft"])
    print("---------------\n")
    if state["hints_given"]:
        print("--- Hints so far ---")
        for i, hint in enumerate(state["hints_given"], 1):
            print(f"{i}. {hint}")
        print("--------------------\n")
    submission = input("Your answer: ")
    return {"submissions": [submission]}

def assessor_node(state: AgentState):
    draft = state["draft"]
    latest_submission = state["submissions"][-1]
    score = llm.invoke(f"You are a fair grader. Question: {draft} Student answer: {latest_submission}. Award 1 if the answer is correct or a valid alternative answer. Award 0 only if clearly wrong. Return only 0 or 1, nothing else.")
    print(f"\n--- Score: {score.content} ---\n")
    return {"scores": [float(score.content)]}

def hint_node(state: AgentState):
    draft = state["draft"]
    latest_submission = state["submissions"][-1]
    previous_hints = state["hints_given"]
    hint = llm.invoke(f"Give a hint for this problem: {draft}. The student submitted: {latest_submission}. Previous hints given: {previous_hints}. Do not repeat previous hints.")
    print(f"\n--- Hint: {hint.content} ---\n")
    return {"hints_given": [hint.content]}