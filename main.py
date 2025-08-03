import argparse
from src.agent.agent import initialize_book_agent
from src.recommendation.book_recommender import recommend_book, simulate_feedback, update_weights
from src.recommendation.state import book_database, state

def validate_preference(value, name):
    try:
        val = float(value)
        if not 0 <= val <= 10:
            raise argparse.ArgumentTypeError(f"{name} must be between 0 and 10, got {val}")
        return val
    except ValueError:
        raise argparse.ArgumentTypeError(f"{name} must be a number, got {value}")

def run_recommendation(preferences):
    try:
        # Update state with user-provided preferences
        state["preferences"] = preferences

        # Initialize the agent
        agent = initialize_book_agent()

        # Step 1: Recommend a book
        prompt = (
            f"User preferences: {state['preferences']}.\n"
            f"Available books: {', '.join(book_database.keys())}.\n"
            f"Use the RecommendBook tool to select a book based on user preferences and current weights.\n"
            f"Format: Action: RecommendBook\nAction Input: Select a book\nFinal Answer: [Book title from tool]"
        )
        response = agent.run(prompt)
        matched_title = next(
            (title for title in book_database if title.lower() == response.lower()),
            None
        )
        if not matched_title:
            print(f"Error: Invalid book title returned: {response}")
            return

        state["recommended_book"] = matched_title

        # Step 2: Generate explanation
        traits = book_database[matched_title]
        explain_prompt = (
            f"User preferences: {state['preferences']}. Book traits: {traits}.\n"
            f"Why is '{matched_title}' a good match? Reply with ONE short sentence.\n"
            f"Do NOT use tools; provide the answer directly.\n"
            f"Format: Final Answer: [One-sentence explanation]"
        )
        explanation = agent.run(explain_prompt).replace("Final Answer: ", "").strip()

        # Step 3: Simulate feedback
        feedback_prompt = (
            f"Use the SimulateFeedback tool to evaluate the recommended book: {matched_title}.\n"
            f"Format: Action: SimulateFeedback\nAction Input: Evaluate {matched_title}\nFinal Answer: [Feedback from tool]"
        )
        feedback = agent.run(feedback_prompt).strip()

        # Step 4: Update weights
        update_prompt = (
            f"Use the UpdateWeights tool to adjust weights based on feedback for {matched_title}.\n"
            f"Format: Action: UpdateWeights\nAction Input: Adjust weights for {matched_title}\nFinal Answer: [Weights from tool]"
        )
        weights = agent.run(update_prompt).strip()

        # Step 5: Print result
        print(f"[Recommendation] {matched_title} | [Reason] {explanation} | [Feedback] {feedback} | [Weights] {weights}")

    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Book Recommendation System")
    parser.add_argument(
        "--creativity",
        type=lambda x: validate_preference(x, "Creativity"),
        required=True,
        help="Preference for creativity (0-10)"
    )
    parser.add_argument(
        "--accuracy",
        type=lambda x: validate_preference(x, "Accuracy"),
        required=True,
        help="Preference for accuracy (0-10)"
    )
    parser.add_argument(
        "--knowledge",
        type=lambda x: validate_preference(x, "Knowledge"),
        required=True,
        help="Preference for knowledge (0-10)"
    )
    args = parser.parse_args()

    preferences = {
        "creativity": args.creativity,
        "accuracy": args.accuracy,
        "knowledge": args.knowledge
    }

    print("=== Recommendation Round ===")
    run_recommendation(preferences)

if __name__ == "__main__":
    main()