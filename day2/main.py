from author_graph import author_app
from validate_graph import validate_app
from assess_graph import assess_app
from hint_graph import hint_app
from adapt_graph import adapt_app
from fastmcp import Client
import asyncio

async def run_tutoring_system(topic: str, student_id: str):
    state = {
        "topic": topic,
        "problem": "",
        "answer": "",
        "submissions": [],
        "scores": [],
        "hints_given": []
    }

    async with Client("mcp_server.py") as client:
        # Step 1: Author + Validate loop
        while True:
            print("\n--- Generating problem... ---\n")
            state = author_app.invoke(state)

            print("\n--- Validating problem... ---\n")
            state = validate_app.invoke(state)

            if state["problem"] and state["answer"]:
                break
            print("\n--- Regenerating... ---\n")

        # Step 2: Save problem to database
        await client.call_tool("save_problem", {
            "topic": topic,
            "problem": state["problem"],
            "answer": state["answer"]
        })

        # Step 3: Assess loop
        while True:
            state = assess_app.invoke(state)
            latest_score = state["scores"][-1]

            if latest_score >= 0.8:
                await client.call_tool("save_score", {
                    "student_id": student_id,
                    "topic": topic,
                    "problem": state["problem"],
                    "score": latest_score,
                    "attempts": len(state["submissions"]),
                    "hints_used": len(state["hints_given"])
                })
                state = adapt_app.invoke(state)
                print("\n--- Well done! ---\n")
                break
            else:
                state = hint_app.invoke(state)

if __name__ == "__main__":
    topic = input("Enter a topic: ")
    student_id = input("Enter your student ID: ")
    asyncio.run(run_tutoring_system(topic, student_id))