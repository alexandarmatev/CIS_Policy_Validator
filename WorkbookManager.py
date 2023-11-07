from Control import Control
import openpyxl


class WorkbookManager:
    _SCOPE_LEVELS = {1, 2}

    def __init__(self, workbook_path):
        self._workbook_path = workbook_path
        self._workbook = openpyxl.load_workbook(self._workbook_path)
        self._cache = None
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

    def _get_worksheet_attributes(self, scope_level):
        worksheet = self._workbook[f'Level {scope_level}']
        header_row = next(worksheet.iter_rows(min_row=1, max_row=1, values_only=True))
        column_indices = {title: index for index, title in enumerate(header_row)}

        return worksheet, header_row, column_indices

    def _populate_cache(self):
        self._cache = {'MacOS L1': {'Sonoma 14.0': []}, 'MacOS L2': {'Sonoma 14.0': []}}
        for level in self._scope_levels:
            worksheet, header_row, column_indices = self._get_worksheet_attributes(level)
            for row in worksheet.iter_rows(min_row=2, values_only=True):
                control_id = row[column_indices['Recommendation #']]
                title = row[column_indices['Title']]
                description = row[column_indices['Description']]
                header = False

                if not control_id:
                    control_id = row[column_indices['Section #']]
                    header = True

                control = Control(control_id, title, description, level, header)
                self._cache[f'MacOS L{level}']['Sonoma 14.0'].append({control_id: control})

    def get_scope_controls(self, *, scope_level=None):
        if (scope_level and scope_level not in self._scope_levels) or not scope_level:
            scope_level = 1
        return self._cache[f'MacOS L{scope_level}']['Sonoma 14.0']

    def get_all_controls(self):
        return self._cache

    def get_control_by_id(self, *, control_level=None, control_id=None):
        if control_level not in self._scope_levels:
            raise ValueError(f'{control_level} is not in the scope levels.')
        if not control_id:
            raise ValueError('Control ID must be provided.')

        control_id = str(control_id)
        scope_controls = self.get_scope_controls(scope_level=control_level)
        control_by_id = (control.get(control_id) for control in scope_controls if control.get(control_id))

        try:
            return next(control_by_id)
        except StopIteration:
            raise KeyError(f'{control_id} is not in the level {control_level} controls.')











