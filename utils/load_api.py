import os
from dotenv import load_dotenv

def load_api_keys(tools:list):
    """
    Load API keys from a .env file located in the root directory.

    Returns:
        dict: A dictionary containing the API keys.
    """
    # Load the .env file
    load_dotenv()

    # Retrieve the API keys
    api_keys = dict()
    for tool in tools:
        if tool=='search':
            api_keys[tool] = os.getenv('SERPER_API_KEY')
        elif tool=='openai':
            api_keys[tool] = os.getenv('OPENAI_API_KEY')    
        else:
            print(f"Don't have API Key for {tool}")
            
    # Check if the keys were loaded successfully
    for key, value in api_keys.items():
        if value is None:
            raise ValueError(f"API key for {key} not found in .env file")

    return api_keys

# Example usage
if __name__ == "__main__":
    api_keys = load_api_keys(['SERPER_API_KEY'])
    print(api_keys)