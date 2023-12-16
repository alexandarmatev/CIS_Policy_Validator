from CISBenchmarksManager import CISBenchmarkManager
from CISControlsManager import CISControlsProcessWorkbook, CISControlsLoadConfig
from AuditCommandManager import AuditCommandManager
from ReportManager import ReportManager
from constants.constants import WORKBOOKS_CONFIG_PATH, JSON_COMMANDS_PATH
from workbook_management.loaders import OpenPyXLWorkbookLoader
from config_management.loaders import JSONConfigLoader

workbook_loader = OpenPyXLWorkbookLoader()
config_loader = JSONConfigLoader()

audit_manager = AuditCommandManager(config_path=WORKBOOKS_CONFIG_PATH, commands_path=JSON_COMMANDS_PATH)

workbook_path = audit_manager.workbook_path
config_path = audit_manager.config_path

cis_controls_config = CISControlsLoadConfig(config_loader=config_loader,
                                            config_path='config/cis_workbooks_config.json')

excel_workbook_loader = OpenPyXLWorkbookLoader()
cis_controls_processor = CISControlsProcessWorkbook(workbook_loader=excel_workbook_loader,
                                                    workbook_path='cis_controls/CIS_Controls_Version_8.xlsx',
                                                    controls_config=cis_controls_config)
workbook = CISBenchmarkManager(workbook_path=workbook_path, config_path=config_path, audit_manager=audit_manager,
                               cis_control_manager=cis_controls_processor)

all_domains_weight = cis_controls_processor.get_all_control_domains_weight()
evaluated_recommendations = workbook.evaluate_recommendations_compliance(scope_level=1)
print(list(evaluated_recommendations))

# report_manager = ReportManager(evaluated_recommendations, all_domains_weight)

# report_manager._create_domains_weight_pie_chart()
# report_manager._create_compliant_recommendations_bar_chart()

# print(report_manager.get_compliant_recommendations_percentage())

# for recommendation in evaluated_recommendations:
#     if recommendation.compliant:
#         print(f'[+] {recommendation.title} - {recommendation.compliant} - {recommendation.cis_control.title}')
#     else:
#         print(f'[-] {recommendation.title} - {recommendation.compliant} - {recommendation.cis_control.title}')

# print(workbook.get_all_levels_recommendations())
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
# print(workbook.get_recommendations_by_level())
#
# # Test get_scope_recommendations for scope level 2
# print(workbook.get_recommendations_by_level(scope_level=2))
#
# # Test get_all_recommendations method
# print(workbook.get_all_levels_recommendations())
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
