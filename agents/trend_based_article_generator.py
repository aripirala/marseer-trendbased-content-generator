from crewai import Agent, Task
# from tools.serper_dev_tool import SerperDevTool, WebsiteSearchTool
import os, sys

# Add the parent directory to the sys.path
current_directory = os.path.dirname(os.path.abspath(__file__))
print(f"cur dir - {current_directory}")

parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

print(f"cur dir - {current_directory}")

from llms.LLM import LLM
# from utils import load_api
from tools.browser_tool import BrowserTools
from tools.search_tools import SearchTools
from tools.trend_listener_tool import TrendListenerTools
from tools.product_analyzer_tool import ProductAnalyzerTool
from tools.content_generator_tool import ContentGeneratorTool
from crewai_tools import JSONSearchTool, DirectorySearchTool, FileReadTool
from textwrap import dedent
from utils.configs import get_agent_config, get_model_config

tools_dict = {
    'search_json': JSONSearchTool(),
    'search_directory': DirectorySearchTool(directory='./data'),
    'search_internet': SearchTools.search_internet,
    'search_instagram': SearchTools.search_instagram,
    'search_facebook': SearchTools.search_facebook,
    'scrape_website': BrowserTools.scrape_and_summarize_website,
    'search_file': FileReadTool(file_path='./data/realistic_products.json'),
    'web_scraper': TrendListenerTools.web_scraper,
    'product_analyzer': ProductAnalyzerTool.product_intelligence_analyzer,
    'content_generator': ContentGeneratorTool.content_generator
}

class Agents:
    def __init__(self):
        pass
        # self.llm = LLM().get_llm()
    
    def TrendListenerAgent(
            self,
    ):
        role, goal, backstory, llm, verbose, max_iter, tools, allow_delegation = self._set_agent_configs('TrendListenerAgent')

        return Agent(role=role,
                     goal=goal,
                     tools=tools,
                     backstory=backstory,
                     llm=llm,
                     max_iter=max_iter,
                     verbose=verbose,
                     allow_delegation=allow_delegation,
                     )
    
    def ProductIntelligenceAgent(self):
        role, goal, backstory, llm, verbose, max_iter, tools, allow_delegation = self._set_agent_configs('ProductIntelligenceAgent')
    
        # llm = LLM(execution_type='openai').get_llm()
        
        return Agent(role=role,
                     goal=goal,
                     tools=tools,
                     backstory=backstory,
                     llm=llm,
                     max_iter=max_iter,
                     verbose=verbose,
                     allow_delegation=allow_delegation,
                     )
    
    def ContentWriterAgent(self):
        role, goal, backstory, llm, verbose, max_iter, tools, allow_delegation = self._set_agent_configs('ContentWriterAgent')
    
        # llm = LLM(execution_type='openai').get_llm()
        
        return Agent(role=role,
                     goal=goal,
                     tools=tools,
                     backstory=backstory,
                     llm=llm,
                     max_iter=max_iter,
                     verbose=verbose,
                     allow_delegation=allow_delegation,
                     )
    
    def BrandStrategistAgent(self):
        role, goal, backstory, llm, verbose, max_iter, tools, allow_delegation = self._set_agent_configs('BrandStrategistAgent')
    
        # llm = LLM(execution_type='openai').get_llm()
        
        return Agent(role=role,
                     goal=goal,
                     tools=tools,
                     backstory=backstory,
                     llm=llm,
                     max_iter=max_iter,
                     verbose=verbose,
                     allow_delegation=allow_delegation,
                     )
   
    def _set_agent_configs(self, agent_name):
        agent_config = get_agent_config()[agent_name]
        role = agent_config['role']
        goal = agent_config['goal']
        backstory = agent_config['backstory']
       
        llm = self._process_llm(agent_config['llm'])
        verbose = agent_config['verbose']
        max_iter = agent_config['max_iter']
        tools = self.get_tools(agent_config['tools'])
        allow_delegation= agent_config['allow_delegation']

        return [role, goal, backstory, llm, verbose, max_iter, tools, allow_delegation]
    
    def _process_llm(self, llm_str):
        model_configs = get_model_config()

        llm_list = llm_str.split('-')

        if len(llm_list) !=2:
            raise Exception(f"LLM - {llm_list} not correctly defined in configs/agent.yaml")
        elif llm_list[0] not in model_configs.keys():
            raise Exception(f"Execution Platform {llm_list[0]} not supported in configs/model.yaml.\
                            \nCurrently only support {model_configs.keys()}")
        elif llm_list[1] not in model_configs[llm_list[0]].keys():
            raise Exception(f"Model {llm_list[1]} not supported in the Execution Platform {llm_list[0]} in configs/model.yaml")
        else:
            print(f"fetching the model")
            return LLM(execution_type=llm_list[0], model=llm_list[1]).get_llm()
        
        # if llm_list[0]=='openai':
        #     # print("Loading OpenAI model")
        #     return LLM(execution_type='openai').get_llm()
        # elif llm_list[1]=='ollama':
        #     #TODO
        #     pass
        # else:
        #     #TODO
        #     pass

    def get_tools(self, tools_identifier_list):
        if tools_identifier_list==[]:
            return []
        tools = [tools_dict[id] for id in tools_identifier_list] 
        return tools
    
if __name__ == '__main__':
    agent = Agents().TrendAnalyzerAgent()