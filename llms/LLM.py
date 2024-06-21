import os
import sys

# Add the parent directory to the sys.path
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from utils.configs import get_model_config
from langchain_openai import ChatOpenAI


class LLM:
    def __init__(self, 
                 execution_type='ollama', 
                 model='llama3',      
                 size='small'           
                 ) -> None:
        
        self.execution_type = execution_type
        self.model = model
        self.size = size
        print(f"Loading {execution_type} ")
    
    def get_llm(self):
        configs = get_model_config()
        if self.execution_type!='openai':

            if self.model not in configs.keys():
                raise Exception(f"Model: {self.model} not defined in the model configs")
            
            model_configs = configs[self.model]            
            if self.execution_type not in model_configs.keys():
                raise Exception(f"For model: {self.model} only support:\n\t {model_configs.keys()}")
            
            if self.size not in model_configs[self.execution_type].keys():
                raise Exception(f"{self.model} - {self.execution_type} - {self.size} not supported yet")
            
        self.set_modelEnv()
        self.set_model()
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

    def set_model(self):
        if os.environ.get('OPENAI_API_BASE'):
            print(os.environ['OPENAI_API_BASE'])
        print(f"API key - {os.environ['OPENAI_API_KEY']}")
        self.llm = ChatOpenAI()
    
    def set_modelEnv(self):
        if self.execution_type.lower()=='ollama':
            os.environ['OPENAI_API_BASE']='http://localhost:11434/v1'
            os.environ['OPENAI_MODEL_NAME'] = self.get_model_name()
            os.environ['OPENAI_API_KEY']='NA'
        elif self.execution_type.lower()=='groq':
            #TODO
            pass
        elif self.execution_type.lower()=='openai':
            os.environ['OPENAI_MODEL_NAME'] = self.get_model_name(model='gpt-3.5')
            # self.model = 'gpt-3.5'            
        else:
            #TODO
            pass


if __name__=='__main__':
    llm = LLM(size='medium', execution_type='groq')
    print(llm.get_llm())