import json
import yaml

def load_json(file_name):
    """Load JSON file with error handling"""
    try:
        with open(file_name) as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load {file_name}: {e}")
        exit(1)

def load_yaml(file_name):
    """Load YAML file with error handling"""
    try:
        with open(file_name) as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load {file_name}: {e}")
        return None

def save_json(data, file_name):
    """Save data to a JSON file with error handling"""
    try:
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Failed to save {file_name}: {e}")

def save_yaml(data, file_name):
    """Save data to a YAML file with error handling"""
    try:
        with open(file_name, 'w') as f:
            yaml.dump(data, f, sort_keys=False)
    except Exception as e:
        print(f"[ERROR] Failed to save {file_name}: {e}")