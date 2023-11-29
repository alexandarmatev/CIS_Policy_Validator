from CISBenchmarkManager import CISBenchmarkManager
from CISControlManager import CISControlManager
from AuditCommandsManager import AuditCommandsManager
from utils.config_load_utils import load_config

WORKBOOKS_CONFIG_PATH = 'config/cis_workbooks_config.json'
general_config = load_config('config/cis_workbooks_config.json')['General Configurations']
COMMANDS_PATH = general_config['COMMANDS_JSON_PATH']
CIS_CONTROLS_PATH = general_config['CIS_CONTROLS_PATH']

audit = AuditCommandsManager(WORKBOOKS_CONFIG_PATH, COMMANDS_PATH)
# audit.run_commands()

workbook_path = audit.workbook_path
# Creating a class instance of WorkbookManager
workbook = CISBenchmarkManager(workbook_path, WORKBOOKS_CONFIG_PATH)
control = CISControlManager(CIS_CONTROLS_PATH, WORKBOOKS_CONFIG_PATH)

print(control.get_all_controls())

print(workbook.config)
print(control.config)

print(workbook.get_all_scopes_recommendations())
print(workbook.get_all_scopes_recommendation_headers())

# Test get_item_by_id method without providing a scope level (default scope level is 1)
print(workbook.get_item_by_id(item_id='1.1', item_type='recommendation'))

# Test get_item_by_id method for getting recommendation and recommendation header for the different control scopes
print(workbook.get_item_by_id(scope_level=1, item_id='1.1', item_type='recommendation'))
print(workbook.get_item_by_id(scope_level=2, item_id='2.1.1.1', item_type='recommendation'))

print(workbook.get_item_by_id(scope_level=1, item_id='1', item_type='recommend_header'))
print(workbook.get_item_by_id(scope_level=2, item_id='2', item_type='recommend_header'))

# Test get_scope_recommendations method without providing a scope level (default scope level is 1)
print(workbook.get_recommendations_scope())

# Test get_scope_recommendations for scope level 2
print(workbook.get_recommendations_scope(scope_level=2))

# Test get_all_recommendations method
print(workbook.get_all_scopes_recommendations())

# Test get_recommendations_scope_headers method without providing a scope level (default scope level is 1)
print(workbook.get_recommendations_scope_headers())

# Test get_recommendations_scope_headers for scope level 2
print(workbook.get_recommendations_scope_headers(scope_level=2))

# Test get_all_recommendation_headers method
print(workbook.get_all_scopes_recommendation_headers())

# Test get recommendations by assessment method
recommendations = workbook.get_recommendations_by_assessment_method(scope_level=1, assessment_method='automated')

for recommendation in recommendations:
    print(recommendation)

print(workbook)