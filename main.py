from dotenv import load_dotenv
load_dotenv()

from crewai import Crew, Task, Process
from agents.trend_based_article_generator import Agents
from tasks.tasks import TrendbasedArticleGeneratorTasks
import json
import os
from utils.helpers import generate_run_id
run_id =  generate_run_id(create_dir=True, output_parent_dir='data')

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
    agents=[trend_listener, product_analyzer, content_writer
            ],
    tasks=[
        # tasks.capture_social_media_trends(agent=trend_listener, output_dir=output_dir, social_media_platforms=['instagram']),
        tasks.task_trend_research(agent=trend_listener, run_id=run_id) , 
        tasks.trend_based_product_analysis(agent=product_analyzer, run_id=run_id),
        tasks.write_engaging_content(agent=content_writer, run_id=run_id),
        # tasks.write_brand_brief(agent=brand_strategist)
    ],
    process=Process.sequential,
    # memory=True,
    verbose=True
)

# Run the crew
if __name__ == "__main__":
    results = crew.kickoff()
    # Define the filename
    # filename = 'trends.json'

    # # Save the JSON data to a file
    # with open(filename, 'w') as file:
    #     json.dump(trend_json, file, indent=4)

    # print(f"Data has been saved to {filename}")

    # Save outputs

    for i, result in enumerate(results[:3], 1):
        with open(f'{output_dir}/task{i}_output.json', 'w') as f:
            json.dump(result, f, indent=4)

    # # Save the last task output as Markdown
    # with open(f'{output_dir}/task4_output.md', 'w') as f:
    #     f.write(results[3])
    print("Task outputs have been saved in the 'task_outputs' directory.")
