from typing import Set
import openpyxl
from utils.config_load_utils import load_config
from utils.validation_utils import validate_and_return_file_path


class ExcelWorkbookBase:
    """
    Base class for managing Excel workbooks. Provides common properties and methods
    for handling Excel workbook operations and configuration management.

    Attributes:
        _workbook_path (str): Path to the Excel workbook file.
        _workbook (openpyxl.Workbook): Instance of the openpyxl Workbook.
        _config_path (str): Path to the JSON configuration file.
        _config (dict): Configuration data specific to the class instance.
        _cache (dict): Cache for storing processed data.
    """
    def __init__(self, workbook_path: str, config_path: str):
        """
        Initializes the ExcelWorkbookBase with paths to an Excel workbook and a JSON configuration file.

        Parameters:
            workbook_path: Path to the Excel workbook file.
            config_path: Path to the JSON configuration file.
        """
        self._workbook_path = validate_and_return_file_path(workbook_path, 'xlsx')
        self._workbook = openpyxl.load_workbook(self._workbook_path)
        self._config_path = validate_and_return_file_path(config_path, 'json')
        self._config = load_config(config_path)[self.__class__.__name__]
        self._cache = {}

    @property
    def config(self) -> dict:
        """
        Gets the configuration data specific to the class instance.

        Returns:
            Configuration data.
        """
        return self._config

    @property
    def config_path(self) -> str:
        """
        Gets the path to the JSON configuration file.

        Returns:
            Path to the configuration file.
        """
        return self._config_path

    @property
    def workbook_path(self) -> str:
        """
        Gets the path to the Excel workbook file.

        Returns:
            Path to the workbook file.
        """
        return self._workbook_path

    @property
    def safeguard(self) -> str:
        """
        Gets the safeguard value from the configuration.

        Returns:
            Safeguard value.
        """
        return self.config['SAFEGUARD']

    @property
    def title(self) -> str:
        """
        Gets the title value from the configuration.

        Returns:
            Title value.
        """
        return self.config['TITLE']

    @property
    def description(self) -> str:
        """
        Gets the description value from the configuration.

        Returns:
            Description value.
        """
        return self.config['DESCRIPTION']

    @property
    def required_column_titles(self) -> Set:
        """
        Gets the set of required column titles from the configuration.

        Returns:
            A set of required column titles.
        """
        return set(self.config['REQUIRED_COLUMN_TITLES'])

    @staticmethod
    def _validate_column_titles(column_indices: dict, required_columns: Set[str]) -> bool:
        """
        Validates if the required columns exist in the provided column indices.

        Parameters:
            column_indices: A dictionary mapping column titles to their respective indices.
            required_columns: A set of required column titles.

        Returns:
            True if validation passes, otherwise raises an AttributeError.

        Raises:
            AttributeError: If any required columns are missing in the column indices.
        """
        columns_to_check = column_indices.keys()
        if not required_columns.issubset(columns_to_check):
            missing_columns = required_columns.difference(columns_to_check)
            raise AttributeError(f"The following columns do not exist in the worksheet: '{', '.join(missing_columns)}'.")
        return True

    def _validate_and_return_sheet_name(self, sheet_name: str) -> str:
        """
        Validates if the given sheet name exists in the workbook and returns it.

        Parameters:
            sheet_name: The name of the sheet to validate.

        Returns:
            The validated sheet name.

        Raises:
            ValueError: If the sheet name is not in the workbook.
        """
        sheetnames_list = self._workbook.sheetnames
        if sheet_name not in sheetnames_list:
            raise ValueError(f'"{sheet_name}" is not in the sheet names. Possible sheet names: {sheetnames_list}.')
        return sheet_name
