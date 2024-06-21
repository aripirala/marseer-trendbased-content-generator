from dotenv import load_dotenv
load_dotenv()

from crewai import Crew, Task, Process
from agents.trend_listener import Agents
from tasks.tasks import TrendbasedArticleGeneratorTasks
# from agents.trend_analyzer import TrendAnalyzerAgent
# from agents.content_writer import ContentWriterAgent
import json
import os
# Load product intelligence data

# with open('data/product_intelligence.json') as f:
    # product_intelligence = json.load(f)
# Create output directory if it doesn't exist
output_dir = 'task_outputs'
os.makedirs(output_dir, exist_ok=True)

agents = Agents()
tasks = TrendbasedArticleGeneratorTasks()

# Initialize agents
trend_listener = agents.TrendListenerAgent()
product_analyzer =  agents.ProductIntelligenceAgent()
content_writer = agents.ContentWriterAgent()
brand_strategist = agents.BrandStrategistAgent()


# Assemble the crew
crew = Crew(
    agents=[trend_listener #, trend_analyzer, content_writer
            ],
    tasks=[
        tasks.capture_social_media_trends(agent=trend_listener, social_media_platforms=['instagram']),
        Task(agent=product_analyzer, description="Analyze trends and map to products", input_data=trend_listener.perform_task(None)),
        # Task(agent=content_writer, description="Generate brand briefs", input_data=trend_analyzer.perform_task(None))
    ],
    process=Process.sequential,
    # memory=True,
    verbose=True
)

# Run the crew
if __name__ == "__main__":
    trend_json = crew.kickoff()
    # Define the filename
    filename = 'trends.json'

    # Save the JSON data to a file
    with open(filename, 'w') as file:
        json.dump(trend_json, file, indent=4)

    print(f"Data has been saved to {filename}")
