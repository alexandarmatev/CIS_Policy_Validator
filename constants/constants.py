from utils.config_load_utils import load_config
from utils.validation_utils import validate_and_return_file_path

WORKBOOKS_CONFIG_PATH = validate_and_return_file_path('config/cis_workbooks_config.json', 'json')
GENERAL_CONFIG = load_config('config/cis_workbooks_config.json')['General Configurations']
COMMANDS_PATH = GENERAL_CONFIG['COMMANDS_JSON_PATH']
CIS_CONTROLS_PATH = GENERAL_CONFIG['CIS_CONTROLS_PATH']