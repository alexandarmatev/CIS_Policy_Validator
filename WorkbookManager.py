from Control import Control
import openpyxl
from collections import namedtuple


class WorkbookManager:
    _SCOPE_LEVELS = {1, 2}

    def __init__(self, workbook_path):
        self._workbook_path = workbook_path
        self._workbook = openpyxl.load_workbook(self._workbook_path)
        self._cache = None
        self._headers = []
        self._scope_levels = WorkbookManager.get_scope_levels()
        self._populate_cache()

    @property
    def path(self):
        return self._workbook_path

    @path.setter
    def path(self, new_path):
        self._workbook_path = new_path
        self._workbook = openpyxl.load_workbook(self._workbook_path)
        self._cache = None
        self._populate_cache()

    @classmethod
    def get_scope_levels(cls):
        return cls._SCOPE_LEVELS

    def _scope_level_validator(self, scope_level):
        if not isinstance(scope_level, int):
            raise ValueError('The scope level must be provided as integer.')
        if scope_level not in self._scope_levels:
            raise ValueError(f'{scope_level} is not in the scope levels.')
        return scope_level

    @staticmethod
    def _control_id_validator(control_id):
        if not isinstance(control_id, str):
            raise TypeError(f'control_id must be a string, got {type(control_id).__name__}')
        return control_id

    def _get_worksheet_attributes(self, scope_level):
        worksheet = self._workbook[f'Level {scope_level}']
        header_row = next(worksheet.iter_rows(min_row=1, max_row=1, values_only=True))
        column_indices = {title: index for index, title in enumerate(header_row)}

        return worksheet, header_row, column_indices

    def _populate_cache(self):
        Header = namedtuple('Header', ['level', 'title', 'description', 'header_id'])
        self._cache = {'MacOS Sonoma L1': [], 'MacOS Sonoma L2': []}
        for level in self._scope_levels:
            worksheet, header_row, column_indices = self._get_worksheet_attributes(level)
            for row in worksheet.iter_rows(min_row=2, values_only=True):
                control_id = row[column_indices['Recommendation #']]
                title = row[column_indices['Title']]
                description = row[column_indices['Description']]
                header = False

                if not control_id:
                    control_id = row[column_indices['Section #']]
                    self._headers.append(Header(level, title, description, control_id))
                    continue

                control = Control(control_id, title, description, level, header)
                self._cache[f'MacOS Sonoma L{level}'].append({control_id: control})

    def get_scope_controls(self, *, scope_level=1):
        scope_level = self._scope_level_validator(scope_level)
        return self._cache[f'MacOS Sonoma L{scope_level}']

    def get_all_controls(self):
        return self._cache

    def get_control_by_id(self, *, scope_level=1, control_id: str):
        scope_level = self._scope_level_validator(scope_level)
        control_id = self._control_id_validator(control_id)

        scope_controls = self.get_scope_controls(scope_level=scope_level)
        control_by_id = (filter(lambda control: control.get(control_id), scope_controls))

        try:
            return next(control_by_id)
        except StopIteration:
            raise KeyError(f'{control_id} is not in the level {scope_level} controls.')

    def get_control_scope_headers(self, *, scope_level=1):
        scope_level = self._scope_level_validator(scope_level)
        return list(filter(lambda control: control.level == scope_level, self._headers))

