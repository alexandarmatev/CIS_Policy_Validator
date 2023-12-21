from abc import ABC, abstractmethod
from typing import Set, List
from workbook_management.interfaces import IWorkbookLoader


class ExcelOpenWorkbook(ABC):
    def __init__(self, workbook_loader: IWorkbookLoader):
        self._workbook_loader = workbook_loader
        self._workbook = self._load_workbook()

    @abstractmethod
    def _load_workbook(self):
        pass


class ExcelValidator(ABC):
    def __init__(self, workbook):
        self._workbook = workbook

    @staticmethod
    @abstractmethod
    def validate_column_titles(column_indices: dict, required_columns: Set[str]) -> bool:
        pass

    @abstractmethod
    def validate_and_return_sheet_name(self, sheet_name: str) -> str:
        pass


class AuditValidator(ABC):
    pass
