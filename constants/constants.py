from utils.config_load_utils import load_config
from utils.validation_utils import validate_and_return_file_path

# Validate and get the absolute path to the CIS workbooks' configuration file.
WORKBOOKS_CONFIG_PATH = validate_and_return_file_path('config/cis_workbooks_config.json', 'json')

# Load the general configuration settings from the specified JSON configuration file.
GENERAL_CONFIG = load_config('config/cis_workbooks_config.json')['General Configurations']

# Extract specific configuration values from the general configuration.
JSON_COMMANDS_PATH = GENERAL_CONFIG['COMMANDS_JSON_PATH']  # Path to the JSON file containing commands.
CIS_CONTROLS_PATH = GENERAL_CONFIG['CIS_CONTROLS_PATH']    # Path to the CIS controls data.
