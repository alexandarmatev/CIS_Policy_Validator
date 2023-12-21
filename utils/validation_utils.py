import os

ALLOWED_EXTENSIONS = {'xlsx', 'json'}


def validate_and_return_file_path(path: str, extension: str) -> str:
    """
    Validates the provided file path for existence, readability, and correct file extension.

    Parameters:
        path: The file path to validate.
        extension: Expected file extension ('xlsx' or 'json').

    Returns:
        The validated file path.

    Raises:
        FileNotFoundError: If the file does not exist or has a wrong extension.
        IsADirectoryError: If the given path is a directory, not a file.
        PermissionError: If the file is not readable.
        ValueError: If the file extension is not correct.
    """
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


def data_type_validator(attr_name: str, attr_value, attr_type: type):
    """
    Validates if the attribute value matches the expected data type.

    Parameters:
        attr_name: The name of the attribute.
        attr_value: The value of the attribute.
        attr_type: The expected type of the attribute.

    Raises:
        TypeError: If the attribute value does not match the expected type.
    """
    if attr_value and not isinstance(attr_value, attr_type):
        raise TypeError(f'Provided argument "{attr_value}" to {attr_name} must be of type {attr_type.__name__}.')
