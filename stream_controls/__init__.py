import yaml

def load_config(file_path='config.yaml'):
    """Load configuration from a YAML file."""
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Load the configuration when the module is imported
CONFIG = load_config()