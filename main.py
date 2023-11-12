from WorkbookManager import WorkbookManager

path = 'cis_benchmarks/CIS_Apple_macOS_14.0_Sonoma_Benchmark_v1.0.0.xlsx'

workbook = WorkbookManager(path)
print(type(workbook))

all_controls = workbook.get_all_recommendations()
print(all_controls)

print(workbook.get_scope_recommendations(scope_level=1))
print(workbook.get_all_recommendation_headers())
recommendation_headers = workbook.get_recommendation_scope_headers()
print(recommendation_headers)
for recommendation in recommendation_headers:
    print(recommendation)

print(workbook.get_item_by_id(scope_level=2, item_id='2.1.1.1', item_type='recommendation'))
