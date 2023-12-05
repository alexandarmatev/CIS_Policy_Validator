from CISBenchmarkManager import CISBenchmarkManager
from CISControlManager import CISControlManager
from AuditCommandManager import AuditCommandManager
from constants.constants import WORKBOOKS_CONFIG_PATH, JSON_COMMANDS_PATH, CIS_CONTROLS_PATH

audit_manager = AuditCommandManager(config_path=WORKBOOKS_CONFIG_PATH, commands_path=JSON_COMMANDS_PATH)
workbook_path = audit_manager.workbook_path
config_path = audit_manager.config_path
cis_control_manager = CISControlManager(workbook_path=CIS_CONTROLS_PATH, config_path=config_path)

workbook = CISBenchmarkManager(workbook_path=workbook_path, config_path=config_path, audit_manager=audit_manager, cis_control_manager=cis_control_manager)

evaluated_recommendations = workbook.evaluate_recommendations_compliance(scope_level=1)

for recommendation in evaluated_recommendations:
    print(f'{recommendation.title} - {recommendation.compliant} - {recommendation.cis_control.title}')


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