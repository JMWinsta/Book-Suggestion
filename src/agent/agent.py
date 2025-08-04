from langchain.agents import Tool, initialize_agent, AgentType
from langchain_ollama import ChatOllama
from src.recommendation.book_recommender import recommend_book, simulate_feedback, update_weights

def initialize_recommendation_agent():
    """Initialize an agent for book recommendation."""
    llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0.5)

    tools = [
        Tool.from_function(
            func=recommend_book,
            name="RecommendBook",
            description="Recommend a book based on user preferences."
        ),
        Tool.from_function(
            func=simulate_feedback,
            name="SimulateFeedback",
            description="Simulate user feedback for a given recommendation."
        ),
        Tool.from_function(
            func=update_weights,
            name="UpdateWeights",
            description="Update the preference weights based on feedback."
        ),
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        handle_parsing_errors=True
    )
    return agent