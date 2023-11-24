from typing import Set, Tuple, Dict, Iterator
from openpyxl.worksheet.worksheet import Worksheet
from ExcelWorkbookBase import ExcelWorkbookBase


class CISControlManager(ExcelWorkbookBase):
    _WORKSHEET_NAME = 'Controls V8'
    _CIS_SAFEGUARD, _ASSET_TYPE, _DOMAIN, _TITLE, _DESCRIPTION = 'CIS Safeguard', 'Asset Type', 'Security Function', 'Title', 'Description'
    _REQUIRED_COLUMN_TITLES = {_CIS_SAFEGUARD, _ASSET_TYPE, _DOMAIN, _TITLE, _DESCRIPTION}

    def __init__(self, workbook_path: str):
        super().__init__(workbook_path)

    @classmethod
    def get_worksheet_name(cls) -> str:
        return cls._WORKSHEET_NAME

    @classmethod
    def get_required_column_titles(cls) -> Set:
        return cls._REQUIRED_COLUMN_TITLES

    def _get_worksheet_scope_headers(self) -> Tuple[Worksheet, Dict[str, int]]:
        worksheet_name = self._validate_and_return_sheet_name(self.get_worksheet_name())
        worksheet = self._workbook[worksheet_name]
        header_row = next(worksheet.iter_rows(min_row=1, max_row=1, values_only=True))
        column_indices = {title: index for index, title in enumerate(header_row)}
        return worksheet, column_indices

    def _get_worksheet_row_attributes(self, worksheet: Worksheet, column_indices: Dict[str, int]) -> Iterator[Tuple[str, str, str, bool]]:
        required_columns = self.get_required_column_titles()
        if self._validate_column_titles(column_indices, required_columns):
            for row in worksheet.iter_rows(min_row=2, values_only=True):
                safeguard_id = row[column_indices[CISControlManager._CIS_SAFEGUARD]]
                asset_type = row[column_indices[CISControlManager._ASSET_TYPE]]
                domain = row[column_indices[CISControlManager._DOMAIN]]
                title = row[column_indices[CISControlManager._TITLE]]
                description = row[column_indices[CISControlManager._DESCRIPTION]]
                is_family = False

                if not asset_type:
                    is_family = True
                    yield title, description, is_family
                else:
                    yield safeguard_id, asset_type, domain, title, description, is_family


controls = CISControlManager('cis_controls/CIS_Controls_Version_8.xlsx')

