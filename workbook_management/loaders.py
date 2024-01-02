import openpyxl
from openpyxl import Workbook
from openpyxl.utils.exceptions import InvalidFileException
from workbook_management.interfaces import IWorkbookLoader
from exceptions.custom_exceptions import WorkbookLoadingError


class OpenPyXLWorkbookLoader(IWorkbookLoader):
    def load(self, path: str) -> Workbook:
        try:
            return openpyxl.load_workbook(path)
        except FileNotFoundError as e:
            raise WorkbookLoadingError(f'Workbook not found {e}')
        except InvalidFileException as e:
            raise WorkbookLoadingError(f'Invalid workbook format: {e}')



