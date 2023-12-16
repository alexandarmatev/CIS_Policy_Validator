import openpyxl
from workbook_management.interfaces import IWorkbookLoader


class OpenPyXLWorkbookLoader(IWorkbookLoader):
    def load(self, path: str):
        return openpyxl.load_workbook(path)


