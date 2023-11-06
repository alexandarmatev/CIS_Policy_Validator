from WorkbookManager import WorkbookManager

workbook = WorkbookManager('cis_benchmarks/CIS_Apple_macOS_14.0_Sonoma_Benchmark_v1.0.0.xlsx')
all_controls = workbook.get_all_scope_controls()

for control in all_controls:
    print(control)
