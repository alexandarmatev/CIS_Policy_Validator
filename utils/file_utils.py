import os


def validate_and_return_file_path(path: str) -> str:
    if not path.endswith('.xlsx'):
        raise FileNotFoundError(f'The file must be a valid xlsx file.')
    if not os.path.exists(path):
        raise FileNotFoundError(f'The file at path {path} does not exist.')
    if not os.path.isfile(path):
        raise IsADirectoryError(f'The path {path} is not a file.')
    if not os.access(path, os.R_OK):
        raise PermissionError(f'The file at path {path} is not readable.')
    if not path.casefold().endswith('.xlsx'):
        raise ValueError(f'The file at path {path} is not a valid Excel workbook file.')
    return path