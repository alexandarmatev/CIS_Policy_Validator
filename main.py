from cis_benchmarks_manager import CISBenchmarksLoadConfig, CISBenchmarksProcessWorkbook
from cis_controls_manager import CISControlsLoadConfig, CISControlsProcessWorkbook
from config_management.loaders import JSONConfigLoader
from workbook_management.loaders import OpenPyXLWorkbookLoader
from cis_audit_manager import CISAuditLoadCommands, CISAuditRunner, CISAuditLoadConfig

CONFIG_PATH = 'config/cis_workbooks_config.json'

json_config_loader = JSONConfigLoader()
openpyxl_workbook_loader = OpenPyXLWorkbookLoader()

cis_audit_config = CISAuditLoadConfig(config_path=CONFIG_PATH, config_loader=json_config_loader)
cis_controls_config = CISControlsLoadConfig(config_loader=json_config_loader, config_path=CONFIG_PATH)
cis_benchmarks_config = CISBenchmarksLoadConfig(config_loader=json_config_loader, config_path=CONFIG_PATH)

COMMANDS_PATH = cis_audit_config.audit_commands_path
CONTROLS_PATH = cis_controls_config.controls_path

cis_controls_processor = CISControlsProcessWorkbook(workbook_loader=openpyxl_workbook_loader,
                                                    workbook_path=CONTROLS_PATH,
                                                    controls_config=cis_controls_config)
all_cis_controls = cis_controls_processor.get_all_controls()

audit_commands_loader = CISAuditLoadCommands(commands_path=COMMANDS_PATH, commands_loader=json_config_loader)

workbook_processor = CISBenchmarksProcessWorkbook(workbook_loader=openpyxl_workbook_loader,
                                                  benchmarks_config=cis_benchmarks_config,
                                                  cis_controls=all_cis_controls,
                                                  commands_loader=audit_commands_loader)

level_1_recommendations = workbook_processor.get_recommendations_by_level(scope_level=2)
all_recommendations = workbook_processor.get_all_levels_recommendations()

cis_audit_runner = CISAuditRunner()
combined_audited_recommendations = cis_audit_runner.evaluate_recommendations_compliance(all_recommendations)

for audited_recommendation in combined_audited_recommendations:
    print(f"[{audited_recommendation.audit_cmd.level}] {audited_recommendation.audit_cmd.title} - {audited_recommendation.compliant}")



