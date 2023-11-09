from DataModels import Control, Header
import openpyxl


class WorkbookManager:
    _SCOPE_LEVELS = {1, 2}

    def __init__(self, workbook_path: str):
        self._workbook_path = workbook_path
        self._workbook = openpyxl.load_workbook(self._workbook_path)
        self._cache = None
        self._headers = None
        self._scope_levels = WorkbookManager.get_scope_levels()
        self._populate_cache_and_headers()

    @property
    def path(self):
        return self._workbook_path

    @path.setter
    def path(self, new_path: str):
        self._workbook_path = new_path
        self._workbook = openpyxl.load_workbook(self._workbook_path)
        self._cache = None
        self._headers = None
        self._populate_cache_and_headers()

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

    def _validate_and_get_items_by_type(self, scope_level, item_type):
        if item_type.casefold() == 'control':
            scope_items = self.get_scope_controls(scope_level=scope_level)
        elif item_type.casefold() == 'header':
            scope_items = self.get_control_scope_headers(scope_level=scope_level)
        else:
            raise KeyError(f'Invalid item type "{item_type}" provided. Item types can be either "control" or "header"')
        return scope_items

    def _get_worksheet_attributes(self, scope_level):
        worksheet = self._workbook[f'Level {scope_level}']
        header_row = next(worksheet.iter_rows(min_row=1, max_row=1, values_only=True))
        column_indices = {title: index for index, title in enumerate(header_row)}

        return worksheet, column_indices

    @staticmethod
    def _get_worksheet_control_attributes(worksheet, column_indices):
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            control_id = row[column_indices['Recommendation #']]
            title = row[column_indices['Title']]
            description = row[column_indices['Description']]
            is_header = False

            if not control_id:
                is_header = True
                control_id = row[column_indices['Section #']]

            yield control_id, title, description, is_header

    def _populate_cache_and_headers(self):
        self._cache = {'MacOS Sonoma L1': [], 'MacOS Sonoma L2': []}
        self._headers = {'level 1': [], 'level 2': []}

        for level in self._scope_levels:
            worksheet, column_indices = self._get_worksheet_attributes(level)
            worksheet_row_attrs = self._get_worksheet_control_attributes(worksheet, column_indices)

            for control_id, title, description, is_header in worksheet_row_attrs:
                if is_header:
                    header_id = control_id
                    header = Header(header_id, title, description, level)
                    self._headers[f'level {level}'].append({header_id: header})
                    continue
                control = Control(control_id, title, description, level)
                self._cache[f'MacOS Sonoma L{level}'].append({control_id: control})

    def get_item_by_id(self, *, scope_level: int = 1, item_id: str, item_type: str):
        scope_level = self._scope_level_validator(scope_level)
        item_id = self._control_id_validator(item_id)
        scope_items = self._validate_and_get_items_by_type(scope_level, item_type)

        for item_dict in scope_items:
            if item_id in item_dict:
                return item_dict[item_id]

        raise KeyError(f'{item_type.capitalize()} with ID {item_id} is not in level {scope_level} of {item_type}s.')

    def get_scope_controls(self, *, scope_level: int = 1):
        scope_level = self._scope_level_validator(scope_level)
        return self._cache[f'MacOS Sonoma L{scope_level}']

    def get_all_controls(self):
        return self._cache

    def get_control_scope_headers(self, *, scope_level: int = 1):
        scope_level = self._scope_level_validator(scope_level)
        return self._headers[f'level {scope_level}']

    def get_all_headers(self):
        return self._headers


