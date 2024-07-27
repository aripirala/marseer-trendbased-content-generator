import os
import sys

# Add the parent directory to the sys.path
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from utils.configs import get_model_config
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq



class LLM:
    def __init__(self, 
                 execution_type_model=None,
                 execution_type='ollama', 
                 model='llama3-8b',        
                 ) -> None:
        if execution_type_model is None:
            self.execution_type = execution_type        
            self.model = model
        else:
            self.execution_type, self.model = execution_type_model.split('-')
            
        print(f"Loading {execution_type}-{model}")
    
    def get_llm(self):
        configs = get_model_config()
        if self.execution_type not in configs.keys():
            raise Exception(f"{self.execution_type} not defined the configs/model.yaml")
        else:
            platform_configs = configs[self.execution_type]
    
        if self.model not in platform_configs.keys():
            raise Exception(f"{self.model} currently not supported within the platform {self.execution_type}")

        model_name = platform_configs[self.model]

        self.set_modelEnv(model_name)
        self.set_model(self.execution_type,model_name)
        return self.llm
    
    def get_model_name(self, model=None):
        if model is None:
            model = self.model
        if self.execution_type=='openai':
            print(get_model_config()[self.execution_type])
            model_name = get_model_config()[self.execution_type][model]
            return model_name
        
        model_configs = get_model_config()[self.model]
        return model_configs[self.execution_type][self.size]

    def set_model(self, execution_type, model_name):
        if execution_type=='openai':
        # if os.environ.get('OPENAI_API_BASE'):
        #     print(os.environ['OPENAI_API_BASE'])
        # print(f"API key - {os.environ['OPENAI_API_KEY']}")
            
            self.llm = ChatOpenAI(model=model_name)
        elif execution_type=='groq':
            self.llm = ChatGroq(model=model_name, api_key=os.getenv("GROQ_API_KEY"))
        else:
            pass

        print(f"Initializing {execution_type}-{model_name}")

    def set_modelEnv(self, model_name):
        if self.execution_type.lower()=='ollama':
            os.environ['OPENAI_API_BASE']='http://localhost:11434/v1'
            os.environ['OPENAI_MODEL_NAME'] = model_name
            os.environ['OPENAI_API_KEY']='NA'
        elif self.execution_type.lower()=='groq':            
            pass
        elif self.execution_type.lower()=='openai':
            os.environ['OPENAI_MODEL_NAME'] = model_name
        else:
            #TODO
            pass


if __name__=='__main__':
    llm = LLM(model='llama3-70b', execution_type='groq')
    print(llm.get_llm())