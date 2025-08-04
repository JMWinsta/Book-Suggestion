import streamlit as st
import json
from langchain_ollama import ChatOllama
from src.recommendation.nlu import parse_preferences
from src.recommendation.state import book_database, state
from src.recommendation.book_recommender import recommend_book, simulate_feedback, update_weights
from fuzzywuzzy import process

# Cache the LLM for explanation
@st.cache_resource
def get_llm():
    return ChatOllama(model="deepseek-r1:1.5b", temperature=0.5)

def save_weights(weights):
    """Save weights to a JSON file."""
    with open("weights.json", "w") as f:
        json.dump(weights, f)

@st.cache_data
def load_weights():
    """Load weights from a JSON file."""
    try:
        with open("weights.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"creativity": 5.0, "accuracy": 5.0, "knowledge": 5.0}

def main():
    st.title("AI Book Recommendation System")
    st.write("Enter your preferences in natural language (e.g., 'I want a creative and informative book').")

    # Input for user preferences
    user_input = st.text_area("Your Preferences", height=100)
    update_weights_toggle = st.checkbox("Update weights based on feedback", value=False)
    if st.button("Get Recommendation"):
        if user_input:
            try:
                # Step 1: Parse preferences using NLU module
                weights = parse_preferences(user_input)
                state["weights"] = weights
                save_weights(weights)
                st.write(f"**Parsed Weights**: {weights}")

                # Step 2: Recommend a book using the tool directly
                response = recommend_book("")
                book_title = response.split("Recommended book:")[-1].split("based on")[0].strip()

                # Fuzzy match to handle partial titles
                matched_title, score = process.extractOne(book_title, book_database.keys())
                if score < 80:
                    st.error(f"Invalid book title returned: {book_title}")
                    return
                state["recommended_book"] = matched_title

                # Step 3: Generate explanation using direct LLM call
                llm = get_llm()
                traits = book_database[matched_title]
                explain_prompt = (
                    f"Weights: {weights}. Book traits: {traits}.\n"
                    f"Why is '{matched_title}' a good match? Reply with ONE short sentence.\n"
                    f"Do not include <think> blocks or additional reasoning.\n"
                    f"Format: [One-sentence explanation]"
                )
                explanation = llm.invoke(explain_prompt).content.strip()

                # Step 4: Simulate feedback using tool directly
                feedback = simulate_feedback("")

                # Step 5: Update weights if toggled
                updated_weights = weights
                if update_weights_toggle:
                    updated_weights = update_weights("")
                    state["weights"] = eval(updated_weights.split("Updated weights: ")[-1])
                    save_weights(state["weights"])

                # Display results
                st.success(f"**Recommendation**: {matched_title}")
                st.write(f"**Reason**: {explanation}")
                st.write(f"**Feedback**: {feedback}")
                if update_weights_toggle:
                    st.write(f"**Updated Weights**: {updated_weights}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()