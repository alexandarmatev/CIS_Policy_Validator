from utils.file_utils import validate_and_return_file_path
import openpyxl
from typing import Set
import json


class ExcelWorkbookBase:
    def __init__(self, workbook_path: str, config_path: str):
        self._workbook_path = self._validate_and_return_file_path(workbook_path, 'xlsx')
        self._config_path = self._validate_and_return_file_path(config_path, 'json')
        self._workbook = openpyxl.load_workbook(self._workbook_path)

    @staticmethod
    def _load_config(config_path: str):
        try:
            with open(config_path, 'r') as config_file:
                return json.load(config_file)
        except json.JSONDecodeError as e:
            raise ValueError(f'Error parsing JSON file at {config_path}: {e}')

    @staticmethod
    def _validate_and_return_file_path(path: str, extension: str) -> str:
        return validate_and_return_file_path(path, extension)

    @staticmethod
    def _validate_column_titles(column_indices: dict, required_columns: Set[str]) -> bool:
        columns_to_check = column_indices.keys()
        if not required_columns.issubset(columns_to_check):
            missing_columns = required_columns.difference(columns_to_check)
            raise AttributeError(f"The following columns do not exist in the worksheet: '{', '.join(missing_columns)}'.")
        return True

    def _validate_and_return_sheet_name(self, sheet_name: str) -> str:
        sheetnames_list = self._workbook.sheetnames
        if sheet_name not in sheetnames_list:
            raise ValueError(f'"{sheet_name}" is not in the sheet names. Possible sheet names: {sheetnames_list}.')
        return sheet_name
