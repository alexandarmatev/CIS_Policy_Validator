import json


def load_config(config_path: str):
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except json.JSONDecodeError as e:
        raise ValueError(f'Error parsing JSON file at {config_path}: {e}')