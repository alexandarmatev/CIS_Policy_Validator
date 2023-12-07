from typing import Tuple, Dict, NamedTuple, List
from openpyxl.worksheet.worksheet import Worksheet
from ExcelWorkbookBase import ExcelWorkbookBase
from DataModels import CISControl, CISControlFamily
from collections import namedtuple


class CISControlManager(ExcelWorkbookBase):
    """
    CISControlManager is a class that extends ExcelWorkbookBase, specialized in managing CIS Controls
    within an Excel workbook. It handles the extraction and organization of CIS control data.

    Attributes:
        _control_families (dict): A dictionary to store CIS control families.
        _cache (dict): A cache to store all CIS controls.
    """

    def __init__(self, workbook_path: str, config_path: str):
        """
        Initializes the CISControlManager with paths to an Excel workbook and a JSON configuration file.

        Parameters:
            workbook_path: Path to the Excel workbook.
            config_path: Path to the configuration file.
        """
        super().__init__(workbook_path, config_path)
        self._control_families = {}
        self._cache = {'All Controls': []}
        self._populate_controls_cache()

    @property
    def worksheet_name(self) -> str:
        """
        Gets the worksheet name from the configuration.

        Returns:
            The name of the worksheet containing CIS control data.
        """
        return self.config['WORKSHEET_NAME']

    @property
    def asset_type(self) -> str:
        """
        Gets the asset type key from the configuration.

        Returns:
            The key for the asset type column in the worksheet.
        """
        return self.config['ASSET_TYPE']

    @property
    def domain(self) -> str:
        """
        Gets the domain key from the configuration.

        Returns:
            The key for the domain column in the worksheet.
        """
        return self.config['DOMAIN']

    @property
    def control_family_id(self) -> str:
        """
        Gets the control family ID key from the configuration.

        Returns:
            The key for the control family ID column in the worksheet.
        """
        return self.config['CONTROL_FAMILY_ID']

    def _get_worksheet_scope_headers(self) -> Tuple[Worksheet, Dict[str, int]]:
        """
        Retrieves the worksheet specified in the configuration and maps the headers to their column indices.

        Returns:
            A tuple containing the worksheet object and a dictionary mapping column titles to indices.
        """
        worksheet_name = self._validate_and_return_sheet_name(self.worksheet_name)
        worksheet = self._workbook[worksheet_name]
        header_row = next(worksheet.iter_rows(min_row=1, max_row=1, values_only=True))
        column_indices = {title: index for index, title in enumerate(header_row)}
        return worksheet, column_indices

    def _get_worksheet_row_attributes(self, worksheet: Worksheet, column_indices: Dict[str, int]) -> NamedTuple:
        """
        Iterates through the rows of the given worksheet and extracts attributes based on the column indices.

        Parameters:
            worksheet: The worksheet object to process.
            column_indices: A dictionary mapping column titles to their indices.

        Returns:
            A generator yielding RowData namedtuples containing CIS control attributes.
        """
        RowData = namedtuple('RowData', ['safeguard_id', 'asset_type', 'domain', 'title', 'description', 'control_family_id', 'is_family'])
        safeguard_ids = set()
        if self._validate_column_titles(column_indices, self.required_column_titles):
            for row in worksheet.iter_rows(min_row=2, values_only=True):
                safeguard_id = str(row[column_indices[self.safeguard]])
                if safeguard_id in safeguard_ids:
                    safeguard_id += '0'
                safeguard_ids.add(safeguard_id)
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
        """
        Populates the controls cache with CIS control data extracted from the worksheet.
        """
        worksheet, column_indices = self._get_worksheet_scope_headers()
        worksheet_row_attrs = self._get_worksheet_row_attributes(worksheet, column_indices)
        for row_data in worksheet_row_attrs:
            if row_data.is_family:
                control_family_id = row_data.control_family_id.strip()
                self._control_families[control_family_id] = CISControlFamily(title=row_data.title, description=row_data.description)
            else:
                self._cache['All Controls'].append(CISControl(safeguard_id=row_data.safeguard_id, asset_type=row_data.asset_type,
                                                              domain=row_data.domain, title=row_data.title, description=row_data.description))

    def get_all_controls(self) -> List[CISControl]:
        """
        Retrieves all CIS controls from the cache.

        Returns:
            A list of CISControl instances representing all controls.
        """
        return self._cache['All Controls']

    def get_all_control_families(self) -> Dict[str, CISControlFamily]:
        """
        Retrieves all CIS control families from the cache.

        Returns:
            A dictionary of CISControlFamily instances representing all control families.
        """
        return self._control_families

    def __repr__(self) -> str:
        """
        Represents the CISControlManager instance as a string.

        Returns:
            A string representation of the CISControlManager instance, including paths to the workbook and configuration file.
        """
        return f'CISControlManager(workbook_path="{self.workbook_path}", config_path="{self.config_path}")'
