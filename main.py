from WorkbookManager import WorkbookManager
import openpyxl

# Path where the benchmark resides
path = 'cis_benchmarks/CIS_Apple_macOS_14.0_Sonoma_Benchmark_v1.0.0.xlsx'

# Creating a class instance of WorkbookManager
workbook = WorkbookManager(path)

print(workbook.get_all_scopes_recommendations())
print(workbook.get_all_scopes_recommendation_headers())

# Test getter method of path
print(workbook.path)

# Test get_scope_levels class method
print(workbook.get_scope_levels())

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
