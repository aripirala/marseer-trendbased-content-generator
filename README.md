# Agentic System for Trend Analysis

This project uses the CrewAI framework to create an agentic system for analyzing trends in the Apparel and Beauty categories from social media platforms.

## Directory Structure

- `agents/`: Contains the agent classes.
- `tools/`: Contains the tools used by the agents.
- `llms/`: Contains the large language model (LLM) classes.
- `data/`: Contains data files such as product intelligence.
- `main.py`: The main script to run the agentic system.
- `requirements.txt`: List of dependencies.
- `README.md`: Project documentation.

## Setup

1. Install dependencies:
    ```bash
    poetry lock
    poetry install
    poetry shell
    ```

2. Run the main script:
    ```bash
    python main.py
    ```

## Agents

- `TrendListenerAgent`: Scrapes social media platforms for trends.
- `TrendAnalyzerAgent`: Maps trends to products and generates relevancy scores.
- `ContentWriterAgent`: Generates brand briefs for top trends.

## Tools

- `SerperDevTool`: Scrapes trends using the Serper Dev API.
- `ProductMappingTool`: Maps trends to products.
- `BrandBriefGeneratorTool`: Generates brand briefs.

## LLMs

- `GPT4`: Organizes trends, analyzes trends, and generates brand briefs.