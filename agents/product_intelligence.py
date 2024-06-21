from crewai import Agent, Task
# from tools.brand_brief_generator_tool import BrandBriefGeneratorTool
from crewai_tools import JSONSearchTool, DirectorySearchTool
from textwrap import dedent

from llms.LLM import LLM

class ProductIntelligenceAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Lead Product Analyst',
            goal=dedent("""\
				Conduct amazing analysis of the products and
				brands, providing in-depth insights to guide
				marketing strategies."""),
			backstory=dedent("""\
				As the Lead Product Analyst at a premier
				digital marketing firm, you specialize in 
                extracting product intelligence through product 
                comparisons, customer feedback, target demography 
                and current trends."""),
            tools=[JSONSearchTool(), DirectorySearchTool()],
            max_iter=10,
            allow_delegation=False,
            verbose=True
        )
        self.llm = LLM(execution_type='openai').get_llm()
        cls.name

    # def perform_task(self, task: Task):
    #     trend_product_mapping = task.input_data
    #     briefs = self.tools[0].generate_brand_briefs(trend_product_mapping)
    #     return briefs
    

if __name__=='__main__':
    pi = ProductIntelligenceAgent()