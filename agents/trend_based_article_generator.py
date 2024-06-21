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
from crewai_tools import JSONSearchTool, DirectorySearchTool
from textwrap import dedent
from utils.configs import get_agent_config

tools_dict = {
    'search_json': JSONSearchTool(),
    'search_directory': DirectorySearchTool(directory='./data'),
    'search_internet': SearchTools.search_internet,
    'search_instagram': SearchTools.search_instagram,
    'search_facebook': SearchTools.search_facebook,
    'scrape_website': BrowserTools.scrape_and_summarize_website
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
    
        llm = LLM(execution_type='openai').get_llm()
        
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
    
        llm = LLM(execution_type='openai').get_llm()
        
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
    
        llm = LLM(execution_type='openai').get_llm()
        
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
        # llm_str = agent_config['llm']
        # print(llm_str)
        llm = self._process_llm(agent_config['llm'])
        verbose = agent_config['verbose']
        max_iter = agent_config['max_iter']
        tools = self.get_tools(agent_config['tools'])
        allow_delegation= agent_config['allow_delegation']

        return [role, goal, backstory, llm, verbose, max_iter, tools, allow_delegation]
    
    def _process_llm(self, llm_str):
        llm_list = llm_str.split('-')
        if llm_list[0]=='openai':
            # print("Loading OpenAI model")
            return LLM(execution_type='openai').get_llm()
        elif llm_list[1]=='ollama':
            #TODO
            pass
        else:
            #TODO
            pass

    def get_tools(self, tools_identifier_list):
        if tools_identifier_list==[]:
            return []
        tools = [tools_dict[id] for id in tools_identifier_list] 
        return tools
    
if __name__ == '__main__':
    agent = Agents().TrendAnalyzerAgent()