from DataModels import Recommendation, RecommendHeader
import openpyxl
import os
from openpyxl.worksheet.worksheet import Worksheet
from typing import Dict, Tuple, Set, List, Iterator


class WorkbookManager:
    _SCOPE_LEVELS = {1, 2}

    def __init__(self, workbook_path: str):
        self._workbook_path = self._validate_and_return_file_path(workbook_path)
        self._workbook = openpyxl.load_workbook(self._workbook_path)
        self._cache = None
        self._headers = None
        self._scope_levels = WorkbookManager.get_scope_levels()
        self._populate_cache_and_headers()

    @staticmethod
    def _validate_and_return_file_path(path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError(f'The file at path {path} does not exist.')
        if not os.path.isfile(path):
            raise IsADirectoryError(f'The path {path} is not a file.')
        if not os.access(path, os.R_OK):
            raise PermissionError(f'The file at path {path} is not readable.')
        if not path.casefold().endswith('.xlsx'):
            raise ValueError(f'The file at path {path} is not a valid Excel workbook file.')
        return path

    @property
    def path(self) -> str:
        return self._workbook_path

    @path.setter
    def path(self, new_path: str):
        self._workbook_path = self._validate_and_return_file_path(new_path)
        self._workbook = openpyxl.load_workbook(self._workbook_path)
        self._cache = None
        self._headers = None
        self._populate_cache_and_headers()

    @classmethod
    def get_scope_levels(cls) -> Set:
        return cls._SCOPE_LEVELS

    def _validate_and_return_scope_level(self, scope_level: int) -> int:
        if not isinstance(scope_level, int):
            raise ValueError('The scope level must be provided as integer.')
        if scope_level not in self._scope_levels:
            raise ValueError(f'{scope_level} is not in the scope levels.')
        return scope_level

    @staticmethod
    def _validate_and_return_item_id(control_id: str) -> str:
        if not isinstance(control_id, str):
            raise TypeError(f'control_id must be a string, got {type(control_id).__name__}')
        return control_id

    def _validate_and_get_items_by_type(self, scope_level: int, item_type: str) -> List[Dict[str, Recommendation]] | List[Dict[str, RecommendHeader]]:
        if item_type.casefold() == 'recommendation':
            scope_items = self.get_scope_recommendations(scope_level=scope_level)
        elif item_type.casefold() == 'recommend_header':
            scope_items = self.get_recommendation_scope_headers(scope_level=scope_level)
        else:
            raise KeyError(f'Invalid item type "{item_type}" provided. Item types can be either "control" or "header".')
        return scope_items

    def _get_worksheet_attributes(self, scope_level: int) -> Tuple[Worksheet, Dict[str, int]]:
        worksheet = self._workbook[f'Level {scope_level}']
        header_row = next(worksheet.iter_rows(min_row=1, max_row=1, values_only=True))
        column_indices = {title: index for index, title in enumerate(header_row)}

        return worksheet, column_indices

    @staticmethod
    def _get_worksheet_recommendation_attributes(worksheet: Worksheet, column_indices: Dict[str, int]) -> Iterator[Tuple[str, str, str, bool]]:
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            recommend_id = row[column_indices['Recommendation #']]
            title = row[column_indices['Title']]
            description = row[column_indices['Description']]
            is_header = False

            if not recommend_id:
                is_header = True
                recommend_id = row[column_indices['Section #']]

            yield recommend_id, title, description, is_header

    def _populate_cache_and_headers(self):
        self._cache = {'MacOS Sonoma L1': [], 'MacOS Sonoma L2': []}
        self._headers = {'level 1': [], 'level 2': []}

        for level in self._scope_levels:
            worksheet, column_indices = self._get_worksheet_attributes(level)
            worksheet_row_attrs = self._get_worksheet_recommendation_attributes(worksheet, column_indices)

            for recommend_id, title, description, is_header in worksheet_row_attrs:
                if is_header:
                    header = RecommendHeader(header_id=recommend_id, title=title, description=description, level=level)
                    self._headers[f'level {level}'].append({recommend_id: header})
                    continue
                recommendation = Recommendation(recommend_id=recommend_id, title=title, description=description, level=level)
                self._cache[f'MacOS Sonoma L{level}'].append({recommend_id: recommendation})

    def get_item_by_id(self, *, scope_level: int = 1, item_id: str, item_type: str) -> Recommendation | RecommendHeader:
        scope_level = self._validate_and_return_scope_level(scope_level)
        item_id = self._validate_and_return_item_id(item_id)
        scope_items = self._validate_and_get_items_by_type(scope_level, item_type)

        for item_dict in scope_items:
            if item_id in item_dict:
                return item_dict[item_id]

        raise KeyError(f'{item_type.capitalize()} with ID {item_id} is not in level {scope_level} of {item_type}s.')

    def get_scope_recommendations(self, *, scope_level: int = 1) -> List[Dict[str, Recommendation]]:
        scope_level = self._validate_and_return_scope_level(scope_level)
        return self._cache[f'MacOS Sonoma L{scope_level}']

    def get_all_recommendations(self) -> Dict[str, List[Dict[str, Recommendation]]]:
        return self._cache

    def get_recommendation_scope_headers(self, *, scope_level: int = 1) -> List[Dict[str, RecommendHeader]]:
        scope_level = self._validate_and_return_scope_level(scope_level)
        return self._headers[f'level {scope_level}']

    def get_all_recommendation_headers(self) -> Dict[str, List[Dict[str, RecommendHeader]]]:
        return self._headers


