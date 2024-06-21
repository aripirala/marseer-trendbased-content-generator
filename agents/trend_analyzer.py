import os
import sys

# Add the parent directory to the sys.path
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)


from crewai import Agent, Task
from tools.product_mapping_tool import ProductMappingTool
from tools.browser_tool import BrowserTools
from tools.search_tools import SearchTools
from llms.LLM import LLM

class TrendAnalyzerAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Trend Analyzer',
            goal='Map trends to products and generate relevancy scores',
            tools=[SearchTools.search_internet],
            max_iter=10,
            verbose=True
        )
        self.llm = LLM().get_llm()

    # def perform_task(self, task: Task):
    #     trends = task.input_data
    #     mapping = self.tools[0].map_trends_to_products(trends)
    #     analyzed_mapping = self.llm.analyze_trends(mapping)
    #     return analyzed_mapping
    
if __name__=='__main__':
    llm = LLM(size='medium', execution_type='groq')
    print(llm.get_llm())