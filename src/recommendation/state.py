book_database = {
    "Thinking, Fast and Slow": {"creativity": 2, "accuracy": 5, "knowledge": 5},
    "The Alchemist": {"creativity": 5, "accuracy": 2, "knowledge": 3},
    "Sapiens": {"creativity": 3, "accuracy": 4, "knowledge": 5},
    "1984": {"creativity": 5, "accuracy": 2, "knowledge": 3},
    "Harry Potter": {"creativity": 5, "accuracy": 3, "knowledge": 2},
}

state = {
    "preferences": {},  # Populated via CLI input
    "recommended_book": "None",
    "feedback": "0.0",
    "weights": {"creativity": 5.0, "accuracy": 5.0, "knowledge": 5.0},
}