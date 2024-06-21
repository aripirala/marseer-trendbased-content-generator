import os
import yaml
from pprint import pprint

# Define the directory where the config files are located
CONFIG_DIR = os.path.join(os.path.dirname(__file__), '../configs')

def load_config(config_name):
    """
    Load a YAML configuration file.
    
    Args:
        config_name (str): The name of the configuration file (without extension).
    
    Returns:
        dict: The contents of the YAML file as a dictionary.
    """
    config_path = os.path.join(CONFIG_DIR, f"{config_name}.yaml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def get_model_config():
    """
    Load the model configuration file.
    
    Returns:
        dict: The contents of the model.yaml file as a dictionary.
    """
    return load_config('model')

def get_agent_config():
    """
    Load the model configuration file.
    
    Returns:
        dict: The contents of the model.yaml file as a dictionary.
    """
    return load_config('agents')


# Example usage
if __name__ == "__main__":
    # model_config = get_model_config()
    agent_config = get_agent_config()

    pprint(agent_config.keys())
