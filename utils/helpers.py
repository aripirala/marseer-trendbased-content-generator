import json
import datetime
import uuid
import os

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{file_path}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    return None

def generate_run_id(prefix=None, suffix=None, create_dir=False, output_parent_dir='data'):
    # Get current timestamp
    timestamp = datetime.datetime.now()
    
    # Format timestamp as a string (YYYYMMDD_HHMMSS)
    timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
    
    # Generate a short UUID
    short_uuid = str(uuid.uuid4())[:8]
    
    if prefix:
        run_id = f"RUN-{prefix}_{timestamp_str}_{short_uuid}"
    else:
    # Combine timestamp and UUID to create run_id
        run_id = f"RUN_{timestamp_str}_{short_uuid}"
    
    if suffix:
        run_id = f"{run_id}-{suffix}"
    if create_dir:
        create_run_directory(run_id, output_parent_dir)

    return run_id

def create_run_directory(run_id, parent_folder):
    # Create the full path for the new directory
    full_path = os.path.join(parent_folder, run_id)
    
    try:
        # Create the directory
        os.makedirs(full_path, exist_ok=True)
        print(f"Directory '{full_path}' created successfully.")
        return full_path
    except PermissionError:
        print(f"Permission denied: Unable to create directory '{full_path}'.")
    except Exception as e:
        print(f"An error occurred while creating directory '{full_path}': {str(e)}")
    
    return None

# Generate and print a run_id
print(f"Generated run_id: {generate_run_id()}")

if __name__=='__main__':
    # file_path = '../data/realistic_products.json'
    # json_data = load_json_file(file_path)

    # if json_data is not None:
    #     print(json_data)

    print(f"run_id:{generate_run_id(create_dir=True)}")