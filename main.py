from CISBenchmarkManager import CISBenchmarkManager
from CISControlManager import CISControlManager
from AuditCommands import AuditCommands

CONFIG_PATH = 'config/cis_workbooks_config.json'
CONTROLS_PATH = 'cis_controls/CIS_Controls_Version_8.xlsx'
audit = AuditCommands(CONFIG_PATH)

audit._add_cmd()
cmd = audit.all_audit_commands[0]
cmd.cmd_output = cmd.function()
print(audit.all_audit_commands)


# # Path where the benchmark resides
# if audit.get_current_os_version() == 'MacOS Ventura':
#     workbook_path = 'cis_benchmarks/CIS_Apple_macOS_13.0_Ventura_Benchmark_v2.0.0.xlsx'
# elif audit.get_current_os_version() == 'MacOS Sonoma':
#     workbook_path = 'cis_benchmarks/CIS_Apple_macOS_14.0_Sonoma_Benchmark_v1.0.0.xlsx'
# else:
#     raise ValueError(f"Mac OS {audit.get_current_os_version()} cannot be audited. Auditable OS versions are: {', '.join(audit.allowed_os_versions)}")
#
#
# # Creating a class instance of WorkbookManager
# workbook = CISBenchmarkManager(workbook_path, CONFIG_PATH)
# control = CISControlManager(CONTROLS_PATH, CONFIG_PATH)
#
# print(control.get_all_controls())
#
# print(workbook.config)
# print(control.config)
#
# print(workbook.get_all_scopes_recommendations())
# print(workbook.get_all_scopes_recommendation_headers())
#
# # Test get_item_by_id method without providing a scope level (default scope level is 1)
# print(workbook.get_item_by_id(item_id='1.1', item_type='recommendation'))
#
# # Test get_item_by_id method for getting recommendation and recommendation header for the different control scopes
# print(workbook.get_item_by_id(scope_level=1, item_id='1.1', item_type='recommendation'))
# print(workbook.get_item_by_id(scope_level=2, item_id='2.1.1.1', item_type='recommendation'))
#
# print(workbook.get_item_by_id(scope_level=1, item_id='1', item_type='recommend_header'))
# print(workbook.get_item_by_id(scope_level=2, item_id='2', item_type='recommend_header'))
#
# # Test get_scope_recommendations method without providing a scope level (default scope level is 1)
# print(workbook.get_recommendations_scope())
#
# # Test get_scope_recommendations for scope level 2
# print(workbook.get_recommendations_scope(scope_level=2))
#
# # Test get_all_recommendations method
# print(workbook.get_all_scopes_recommendations())
#
# # Test get_recommendations_scope_headers method without providing a scope level (default scope level is 1)
# print(workbook.get_recommendations_scope_headers())
#
# # Test get_recommendations_scope_headers for scope level 2
# print(workbook.get_recommendations_scope_headers(scope_level=2))
#
# # Test get_all_recommendation_headers method
# print(workbook.get_all_scopes_recommendation_headers())
#
# # Test get recommendations by assessment method
# recommendations = workbook.get_recommendations_by_assessment_method(scope_level=1, assessment_method='automated')
#
# for recommendation in recommendations:
#     print(recommendation)
#
# print(workbook)