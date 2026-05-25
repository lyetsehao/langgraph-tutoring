from author_graph import author_app
from validate_graph import validate_app
from assess_graph import assess_app
from hint_graph import hint_app
from adapt_graph import adapt_app

def run_tutoring_system(topic: str):
    state = {
        "topic": topic,
        "problem": "",
        "answer": "",
        "submissions": [],
        "scores": [],
        "hints_given": []
    }

    # Step 1: Author generates problem and answer
    print("\n--- Generating problem... ---\n")
    state = author_app.invoke(state)

    # Step 2: Validate the problem
    print("\n--- Validating problem... ---\n")
    state = validate_app.invoke(state)

    # Step 3: Assess loop
    while True:
        state = assess_app.invoke(state)
        latest_score = state["scores"][-1]

        if latest_score >= 0.8:
            # Step 4: Adapt difficulty
            state = adapt_app.invoke(state)
            print("\n--- Well done! ---\n")
            break
        else:
            # Step 4: Give hint and loop back
            state = hint_app.invoke(state)

if __name__ == "__main__":
    topic = input("Enter a topic: ")
    run_tutoring_system(topic)