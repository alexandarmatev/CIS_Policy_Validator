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


def data_type_validator(attr_name, attr_value, attr_type):
    if attr_value and not isinstance(attr_value, attr_type):
        raise TypeError(f'Provided argument "{attr_value}" to {attr_name} must be of type {attr_type.__name__}.')


def cmd_output_validate_and_return(cmd_result):
    output_code = cmd_result.returncode
    if output_code != 0:
        cmd_stderr = cmd_result.stderr.decode('UTF-8').strip()
        raise RuntimeError(f"Command failed with error: '{cmd_stderr}'")
    return cmd_result.stdout.decode('UTF-8').split('\n')

