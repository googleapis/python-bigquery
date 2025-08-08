# config_helper.py

import yaml
import os


def load_config_yaml(filepath):
    """Loads configuration from a YAML file."""
    try:
        with open(filepath, "r") as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{filepath}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error: Could not load YAML from '{filepath}': {e}")
        return None


# Determine the absolute path to the config file relative to this file.
# This makes the path robust to where the script is run from.
_CONFIG_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "bigqueryclient_config.yaml"
)

config_data = load_config_yaml(_CONFIG_FILE_PATH)

if config_data:
    CLASSES_TO_INCLUDE = config_data.get("include_class_name_patterns", [])
    CLASSES_TO_EXCLUDE = config_data.get("exclude_class_name_patterns", [])
    METHODS_TO_INCLUDE = config_data.get("include_method_name_patterns", [])
    METHODS_TO_EXCLUDE = config_data.get("exclude_method_name_patterns", [])
else:
    # Define default empty values if the config fails to load
    CLASSES_TO_INCLUDE = []
    CLASSES_TO_EXCLUDE = []
    METHODS_TO_INCLUDE = []
    METHODS_TO_EXCLUDE = []
