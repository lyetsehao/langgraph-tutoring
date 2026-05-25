from langgraph.graph import StateGraph, END
from state import AgentState
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os
import json

load_dotenv()

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

import random

def author_node(state: AgentState):
    topic = state["topic"]
    style = random.choice([
        "an obscure and less known fact",
        "a surprising or counterintuitive fact",
        "a record-breaking fact",
        "a historical fact",
        "a scientific fact"
    ])
    response = llm.invoke(
        f"Create a trivia question about {topic} based on {style}. "
        f"You must respond with ONLY a JSON object, no other text, no markdown, no backticks. "
        f"Example: {{\"problem\": \"What is the capital of France?\", \"answer\": \"Paris\"}}"
    )
    content = response.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    data = json.loads(content.strip())
    return {
        "problem": data["problem"],
        "answer": data["answer"]
    }

graph = StateGraph(AgentState)
graph.add_node("author", author_node)
graph.set_entry_point("author")
graph.add_edge("author", END)

author_app = graph.compile()