from langchain.tools import tool
from .state import book_database, state

@tool
def recommend_book() -> str:
    """Recommend the best book based on weighted user preferences."""
    weights = state["weights"]
    scores = {}
    for book, traits in book_database.items():
        score = sum(weights.get(k, 0) * traits.get(k, 0) for k in traits)
        scores[book] = score
    best_book = max(scores, key=scores.get)
    state["recommended_book"] = best_book
    return f"Recommended book: {best_book} based on weights {weights}"

@tool
def simulate_feedback() -> str:
    """Simulate user feedback based on how well the recommended book aligns with preferences."""
    book = state["recommended_book"]
    prefs = state["preferences"]
    traits = book_database.get(book, {})
    alignment = sum(
        1 if traits.get(k, 0) >= prefs.get(k, 5) else -1
        for k in prefs
    )
    feedback = "good" if alignment >= 0 else "bad"
    state["feedback"] = feedback
    return f"User gave '{book}' a feedback: {feedback}"

@tool
def update_weights() -> str:
    """Update weights based on feedback to improve future recommendations."""
    feedback = state["feedback"]
    book = state["recommended_book"]
    traits = book_database[book]
    adjustment = 1 if feedback == "good" else -1

    for k in state["weights"]:
        delta = 0.1 * adjustment * traits.get(k, 0)
        state["weights"][k] += delta
        state["weights"][k] = max(0.0, min(10.0, state["weights"][k]))
    return f"Updated weights: {state['weights']}"