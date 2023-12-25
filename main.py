from CISBenchmarksManager import CISBenchmarksLoadConfig, CISBenchmarksProcessWorkbook
from CISControlsManager import CISControlsLoadConfig, CISControlsProcessWorkbook
from config_management.loaders import JSONConfigLoader
from workbook_management.loaders import OpenPyXLWorkbookLoader
from CISAuditManager import CISAuditLoadCommands, CISAuditRunner, CISAuditLoadConfig

CONFIG_PATH = 'config/cis_workbooks_config.json'

json_config_loader = JSONConfigLoader()
openpyxl_workbook_loader = OpenPyXLWorkbookLoader()

cis_audit_config = CISAuditLoadConfig(config_path=CONFIG_PATH, config_loader=json_config_loader)
COMMANDS_PATH = cis_audit_config.audit_commands_path

cis_controls_config = CISControlsLoadConfig(config_loader=json_config_loader, config_path=CONFIG_PATH)
CONTROLS_PATH = cis_controls_config.controls_path

cis_controls_processor = CISControlsProcessWorkbook(workbook_loader=openpyxl_workbook_loader,
                                                    workbook_path=CONTROLS_PATH,
                                                    controls_config=cis_controls_config)
all_cis_controls = cis_controls_processor.get_all_controls()

cis_benchmarks_config = CISBenchmarksLoadConfig(config_loader=json_config_loader, config_path=CONFIG_PATH)

audit_commands_loader = CISAuditLoadCommands(commands_path=COMMANDS_PATH, commands_loader=json_config_loader)

workbook_processor = CISBenchmarksProcessWorkbook(workbook_loader=openpyxl_workbook_loader,
                                                  benchmarks_config=cis_benchmarks_config,
                                                  cis_controls=all_cis_controls,
                                                  commands_loader=audit_commands_loader)

level_1_recommendations = workbook_processor.get_recommendations_by_level(scope_level=1)

cis_audit_runner = CISAuditRunner()
level_1_audited_recommendations = cis_audit_runner.evaluate_recommendations_compliance(recommendations=level_1_recommendations)

for audited_recommendation in level_1_audited_recommendations:
    print(f"{audited_recommendation.audit_cmd.title} - {audited_recommendation.compliant}")



