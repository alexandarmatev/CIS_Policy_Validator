from WorkbookManager import WorkbookManager

workbook = WorkbookManager('cis_benchmarks/CIS_Apple_macOS_14.0_Sonoma_Benchmark_v1.0.0.xlsx')
all_controls = workbook.get_all_scope_controls()

print(workbook.get_scope_controls(scope_level=1))
print(workbook.get_control_by_id(control_level=2, control_id=1))