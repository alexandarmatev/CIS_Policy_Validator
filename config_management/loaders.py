from typing import Dict
from config_management.interfaces import IConfigLoader
import json


class JSONConfigLoader(IConfigLoader):
    def load(self, path: str) -> Dict:
        try:
            with open(path, 'r') as config_file:
                return json.load(config_file)
        except json.JSONDecodeError as e:
            raise ValueError(f'Error parsing JSON file at {path}: {e}')