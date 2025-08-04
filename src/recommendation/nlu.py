import spacy
import streamlit as st

# Cache spaCy model
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

def parse_preferences(text):
    """Parse natural language preferences using spaCy and return weights."""
    doc = nlp(text.lower())
    weights = {"creativity": 5.0, "accuracy": 5.0, "knowledge": 5.0}
    for token in doc:
        if token.text in ["creative", "imaginative", "original"]:
            weights["creativity"] = min(weights["creativity"] + 2, 10.0)
        elif token.text in ["accurate", "factual", "precise"]:
            weights["accuracy"] = min(weights["accuracy"] + 2, 10.0)
        elif token.text in ["informative", "educational", "knowledgeable"]:
            weights["knowledge"] = min(weights["knowledge"] + 2, 10.0)
        elif token.text in ["less", "not"]:
            for prev in doc[:token.i]:
                if prev.text in ["creative", "imaginative"]:
                    weights["creativity"] = max(weights["creativity"] - 2, 0.0)
                elif prev.text in ["accurate", "factual"]:
                    weights["accuracy"] = max(weights["accuracy"] - 2, 0.0)
                elif prev.text in ["informative", "educational"]:
                    weights["knowledge"] = max(weights["knowledge"] - 2, 0.0)
    return weights