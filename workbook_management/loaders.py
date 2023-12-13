import openpyxl
import json
from workbook_management.interfaces import IConfigLoader, IWorkbookLoader


class OpenPyXLWorkbookLoader(IWorkbookLoader):
    def load(self, path: str):
        return openpyxl.load_workbook(path)


class JSONConfigLoader(IConfigLoader):
    def load(self, path: str):
        try:
            with open(path, 'r') as config_file:
                return json.load(config_file)
        except json.JSONDecodeError as e:
            raise ValueError(f'Error parsing JSON file at {path}: {e}')
