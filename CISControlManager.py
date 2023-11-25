from typing import Set, Tuple, Dict, Iterator
from openpyxl.worksheet.worksheet import Worksheet
from ExcelWorkbookBase import ExcelWorkbookBase


class CISControlManager(ExcelWorkbookBase):

    def __init__(self, workbook_path: str, config_path: str):
        super().__init__(workbook_path, config_path)
        self._config = self._load_config(config_path)[__class__.__name__]

    @property
    def worksheet_name(self) -> str:
        return self.config['WORKSHEET_NAME']

    @property
    def asset_type(self) -> str:
        return self.config['ASSET_TYPE']

    @property
    def domain(self) -> str:
        return self.config['DOMAIN']

    def _get_worksheet_scope_headers(self) -> Tuple[Worksheet, Dict[str, int]]:
        worksheet_name = self._validate_and_return_sheet_name(self.worksheet_name)
        worksheet = self._workbook[worksheet_name]
        header_row = next(worksheet.iter_rows(min_row=1, max_row=1, values_only=True))
        column_indices = {title: index for index, title in enumerate(header_row)}
        return worksheet, column_indices

    def _get_worksheet_row_attributes(self, worksheet: Worksheet, column_indices: Dict[str, int]) -> Iterator[Tuple[str, str, str, bool]]:
        required_columns = self.required_column_titles
        if self._validate_column_titles(column_indices, required_columns):
            for row in worksheet.iter_rows(min_row=2, values_only=True):
                safeguard_id = row[column_indices[self.safeguard]]
                asset_type = row[column_indices[self.asset_type]]
                domain = row[column_indices[self.domain]]
                title = row[column_indices[self.title]]
                description = row[column_indices[self.description]]
                is_family = False

                if not asset_type:
                    is_family = True
                    yield title, description, is_family
                else:
                    yield safeguard_id, asset_type, domain, title, description, is_family

    def __repr__(self):
        return f'CISControlManager(workbook_path="{self.workbook_path}", config_path="{self.config_path}")'
