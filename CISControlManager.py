from typing import Tuple, Dict, NamedTuple
from openpyxl.worksheet.worksheet import Worksheet
from ExcelWorkbookBase import ExcelWorkbookBase
from DataModels import CISControl, CISControlFamily
from collections import namedtuple


class CISControlManager(ExcelWorkbookBase):
    def __init__(self, workbook_path: str, config_path: str):
        super().__init__(workbook_path, config_path)
        self._control_families = {}
        self._populate_controls_cache()

    @property
    def worksheet_name(self) -> str:
        return self.config['WORKSHEET_NAME']

    @property
    def asset_type(self) -> str:
        return self.config['ASSET_TYPE']

    @property
    def domain(self) -> str:
        return self.config['DOMAIN']

    @property
    def control_family_id(self) -> str:
        return self.config['CONTROL_FAMILY_ID']

    def _get_worksheet_scope_headers(self) -> Tuple[Worksheet, Dict[str, int]]:
        worksheet_name = self._validate_and_return_sheet_name(self.worksheet_name)
        worksheet = self._workbook[worksheet_name]
        header_row = next(worksheet.iter_rows(min_row=1, max_row=1, values_only=True))
        column_indices = {title: index for index, title in enumerate(header_row)}
        return worksheet, column_indices

    def _get_worksheet_row_attributes(self, worksheet: Worksheet, column_indices: Dict[str, int]) -> NamedTuple:
        RowData = namedtuple('RowData', ['safeguard_id', 'asset_type', 'domain', 'title', 'description', 'control_family_id', 'is_family'])
        if self._validate_column_titles(column_indices, self.required_column_titles):
            for row in worksheet.iter_rows(min_row=2, values_only=True):
                safeguard_id = str(row[column_indices[self.safeguard]])
                asset_type = row[column_indices[self.asset_type]]
                domain = row[column_indices[self.domain]]
                title = row[column_indices[self.title]]
                description = row[column_indices[self.description]]
                control_family_id = None
                is_family = False

                if not asset_type:
                    is_family = True
                    control_family_id = str(row[column_indices[self.control_family_id]])

                yield RowData(safeguard_id, asset_type, domain, title, description, control_family_id, is_family)

    def _populate_controls_cache(self):
        worksheet, column_indices = self._get_worksheet_scope_headers()
        worksheet_row_attrs = self._get_worksheet_row_attributes(worksheet, column_indices)
        for row_data in worksheet_row_attrs:
            if row_data.is_family:
                self._control_families[row_data.control_family_id] = CISControlFamily(title=row_data.title, description=row_data.description)
            else:
                self._cache[row_data.safeguard_id] = CISControl(safeguard_id=row_data.safeguard_id, asset_type=row_data.asset_type,
                                                                domain=row_data.domain, title=row_data.title, description=row_data.description)

    def get_all_controls(self):
        return self._cache

    def __repr__(self):
        return f'CISControlManager(workbook_path="{self.workbook_path}", config_path="{self.config_path}")'
