import os

ALLOWED_EXTENSIONS = {'xlsx', 'json'}


def validate_and_return_file_path(path: str, extension: str) -> str:
    if extension not in ALLOWED_EXTENSIONS:
        raise FileNotFoundError(f'"{extension}" is not allowed extension. Allowed extensions: {ALLOWED_EXTENSIONS}')
    if not os.path.exists(path):
        raise FileNotFoundError(f'The file at path {path} does not exist.')
    if not os.path.isfile(path):
        raise IsADirectoryError(f'The path {path} is not a file.')
    if not os.access(path, os.R_OK):
        raise PermissionError(f'The file at path {path} is not readable.')
    if extension == 'xlsx':
        if not path.casefold().endswith('.xlsx'):
            raise ValueError(f'The file at path {path} is not a valid Excel workbook file.')
    if extension == 'json':
        if not path.casefold().endswith('.json'):
            raise ValueError(f'The file at path {path} is not a valid json file.')
    return path
