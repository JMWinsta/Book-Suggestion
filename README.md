# Book Recommendation System
A simple Agentic AI framework that suggests books based on meta reasoning. This project implements a book recommendation system using LangChain, LangGraph, and a local Ollama LLM (deepseek-r1:1.5b). The system recommends books based on user preferences for creativity, accuracy, and knowledge, simulates feedback, and updates recommendation weights.
## Description
Agentic AI refers to autonomous systems that proactively make decisions and adapt based on goals and environmental feedback. In this project, an agentic AI is built using LangChain's agent framework, leveraging a local Ollama LLM (deepseek-r1:1.5b) to orchestrate a book recommendation process. The agent employs tools to recommend books, simulate user feedback, and adjust preference weights dynamically, mimicking human-like decision-making. Meta-reasoning, the process of reasoning about reasoning, is integral to the agent's operation. The LLM evaluates its own recommendation logic by comparing book traits against user preferences, as seen in the verbose reasoning logs during book selection. This introspective capability allows the agent to justify choices, such as selecting "The Creative Mind" for its high creativity score, despite minor mismatches in accuracy. By integrating meta-reasoning, the system ensures recommendations align with user needs while learning from feedback to refine future suggestions. The combination of agentic AI and meta-reasoning creates a robust, adaptive system capable of iterative improvement, showcasing practical applications in personalized recommendation tasks.

## Files

test_alpha.ipynb: Jupyter notebook containing the implementation, including book database, tools, and agent logic.

## Setup

Install dependencies:pip install langchain langgraph langchain_ollama


Ensure Ollama is running locally with the deepseek-r1:1.5b model.

## Usage
Run test4.ipynb in a Jupyter environment to execute the recommendation system for three rounds, displaying book choices and reasons.
Requirements

Python 3.10+
Jupyter Notebook
Ollama with deepseek-r1:1.5b
Libraries: langchain, langgraph, langchain_ollama

## Future Enhancements

Dynamic User Input: Allow real-time user preference input instead of static preferences.
Expanded Book Database: Integrate a larger, external book database via APIs (e.g., Google Books).
Advanced Feedback Mechanism: Implement nuanced feedback scores (e.g., 1-10) for finer weight adjustments.
Model Optimization: Use a more powerful LLM (e.g., LLaMA) for improved reasoning accuracy.
Visualization: Add plots to visualize preference alignment and weight changes over rounds.

