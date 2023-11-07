from Control import Control
import openpyxl


class WorkbookManager:
    _SCOPE_LEVELS = {1, 2}

    def __init__(self, workbook_path):
        self._workbook_path = workbook_path
        self._workbook = openpyxl.load_workbook(self._workbook_path)

    @property
    def path(self):
        return self._workbook_path

    @path.setter
    def path(self, new_path):
        self._workbook_path = new_path
        self._workbook = openpyxl.load_workbook(self._workbook_path)

    @classmethod
    def get_scope_levels(cls):
        return cls._SCOPE_LEVELS

    def _get_worksheet_attributes(self, scope_level):
        worksheet = self._workbook[f'Level {scope_level}']
        header_row = next(worksheet.iter_rows(min_row=1, max_row=1, values_only=True))
        column_indices = {title: index for index, title in enumerate(header_row)}

        return worksheet, header_row, column_indices

    def get_all_scope_controls(self, scope_level=None):
        scope_levels = WorkbookManager.get_scope_levels()

        if (scope_level and scope_level not in scope_levels) or not scope_level:
            scope_level = 1

        worksheet, header_row, column_indices = self._get_worksheet_attributes(scope_level)

        all_scope_controls = []
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            control_id = row[column_indices['Recommendation #']]
            title = row[column_indices['Title']]
            description = row[column_indices['Description']]
            level = scope_level
            header = False

            if not control_id:
                control_id = row[column_indices['Section #']]
                header = True

            control = Control(control_id, title, description, level, header)
            all_scope_controls.append(control)

        return all_scope_controls










