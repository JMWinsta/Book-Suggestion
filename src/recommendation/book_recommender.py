from langchain.tools import tool
from .state import book_database, state

@tool
def recommend_book(tool_input: str = "") -> str:
    """Recommend the best book based on weighted user preferences."""
    print(f"recommend_book called with input: {tool_input}")  # Debugging
    weights = state["weights"]
    scores = {}
    for book, traits in book_database.items():
        score = sum(weights.get(k, 0) * traits.get(k, 0) for k in traits)
        scores[book] = score
    best_book = max(scores, key=scores.get)
    state["recommended_book"] = best_book
    return f"Recommended book: {best_book} based on weights {weights}"

@tool
def simulate_feedback(tool_input: str = "") -> str:
    """Simulate user feedback based on how well the recommended book aligns with preferences."""
    print(f"simulate_feedback called with input: {tool_input}")  # Debugging
    book = state["recommended_book"]
    prefs = state["weights"]
    traits = book_database.get(book, {})
    # Calculate weighted alignment score
    total_score = sum(prefs.get(k, 0) * traits.get(k, 0) for k in prefs)
    max_score = sum(prefs.get(k, 0) * 5 for k in prefs)  # Max trait value is 5
    alignment = total_score / max_score if max_score > 0 else 0
    feedback = "good" if alignment >= 0.6 else "bad"  # Threshold for "good" feedback
    state["feedback"] = feedback
    return f"User gave '{book}' a feedback: {feedback}"

@tool
def update_weights(tool_input: str = "") -> str:
    """Update weights based on feedback to improve future recommendations."""
    print(f"update_weights called with input: {tool_input}")  # Debugging
    feedback = state["feedback"]
    book = state["recommended_book"]
    traits = book_database[book]
    adjustment = 0.5 if feedback == "good" else -0.5  # Adjusted for moderate updates

    for k in state["weights"]:
        delta = adjustment * traits.get(k, 0) * 0.1
        state["weights"][k] += delta
        state["weights"][k] = max(0.0, min(10.0, state["weights"][k]))
    return f"Updated weights: {state['weights']}"