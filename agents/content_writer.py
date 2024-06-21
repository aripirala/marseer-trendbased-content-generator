from crewai import Agent, Task
from tools.brand_brief_generator_tool import BrandBriefGeneratorTool
from llms.gpt4 import GPT4

class ContentWriterAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Content Writer',
            goal='Generate brand briefs for top trends',
            tools=[BrandBriefGeneratorTool()],
            max_iter=10,
            verbose=True
        )
        self.llm = GPT4()

    def perform_task(self, task: Task):
        trend_product_mapping = task.input_data
        briefs = self.tools[0].generate_brand_briefs(trend_product_mapping)
        return briefs