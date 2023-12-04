import json


def load_config(config_path: str) -> dict:
    """
    Loads configuration data from a JSON file.

    Parameters:
        config_path: The path to the JSON configuration file.

    Returns:
        A dictionary representing the loaded configuration data.

    Raises:
        ValueError: If there is an error parsing the JSON file.
    """
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except json.JSONDecodeError as e:
        raise ValueError(f'Error parsing JSON file at {config_path}: {e}')