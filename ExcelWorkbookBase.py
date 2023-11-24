from utils.file_utils import validate_and_return_file_path
import openpyxl
from typing import Set


class ExcelWorkbookBase:
    def __init__(self, workbook_path: str):
        self._workbook_path = self._validate_and_return_file_path(workbook_path)
        self._workbook = openpyxl.load_workbook(self._workbook_path)

    @staticmethod
    def _validate_and_return_file_path(path: str) -> str:
        return validate_and_return_file_path(path)

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
