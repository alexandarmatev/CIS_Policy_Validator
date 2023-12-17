import json
from enum import Enum
import openpyxl
from DataModels import Recommendation, RecommendHeader, AuditCmd
from config_management.interfaces import IConfigLoader
from config_management.loaders import JSONConfigLoader
from workbook_management.excel_workbook_manager import ExcelOpenWorkbook, ExcelValidator
from AuditCommandManager import AuditCommandManager
from CISControlsManager import CISControlsProcessWorkbook
import re
from collections import defaultdict
from openpyxl.worksheet.worksheet import Worksheet
from typing import Dict, Tuple, Set, List, Iterator, Generator
from utils.validation_utils import validate_and_return_file_path
from workbook_management.interfaces import IWorkbookLoader
from config_management.config_manager import BenchmarkConfigAttrs
from workbook_management.loaders import OpenPyXLWorkbookLoader


class CISBenchmarksConst(Enum):
    CIS_BENCHMARKS_CONFIG = 'CISBenchmarksManager'


class CISBenchmarksLoadConfig(BenchmarkConfigAttrs):
    def __init__(self, *, config_path: str, config_loader: IConfigLoader):
        self._config_path = validate_and_return_file_path(config_path, 'json')
        self._config_title = CISBenchmarksConst.CIS_BENCHMARKS_CONFIG.value
        super().__init__(config_loader)

    def _load_config(self) -> dict:
        config = self._config_loader.load(self._config_path).get(self._config_title)
        if config:
            return config
        raise KeyError('This configuration does not exist within the configuration file.')

    @property
    def scope_levels(self) -> dict:
        scope_levels = {int(level): title for level, title in self._config.get('SCOPE_LEVELS').items()}
        if scope_levels:
            return scope_levels
        raise KeyError('The key does not exist within the configuration file.')

    @property
    def allowed_assessment_methods(self) -> list:
        allowed_assessment_methods = self._config.get('ALLOWED_ASSESSMENT_METHODS')
        if allowed_assessment_methods:
            return allowed_assessment_methods
        raise KeyError('The key does not exist within the configuration file.')

    @property
    def benchmark_profiles_rex(self) -> str:
        benchmark_profiles_rex = self._config.get('BENCHMARK_PROFILES_REX')
        if benchmark_profiles_rex:
            return benchmark_profiles_rex
        raise KeyError('The key does not exist within the configuration file.')

    @property
    def section(self) -> str:
        section = self._config.get('SECTION')
        if section:
            return section
        raise KeyError('The key does not exist within the configuration file.')

    @property
    def recommendation(self) -> str:
        recommendation = self._config.get('RECOMMENDATION')
        if recommendation:
            return recommendation
        raise KeyError('The key does not exist within the configuration file.')

    @property
    def title(self) -> str:
        title = self._config.get('TITLE')
        if title:
            return title
        raise KeyError('The key does not exist within the configuration file.')

    @property
    def assessment_status(self) -> str:
        assessment_status = self._config.get('ASSESSMENT_STATUS')
        if assessment_status:
            return assessment_status
        raise KeyError('The key does not exist within the configuration file.')

    @property
    def description(self) -> str:
        description = self._config.get('DESCRIPTION')
        if description:
            return description
        raise KeyError('The key does not exist within the configuration file.')

    @property
    def rationale(self) -> str:
        rationale = self._config.get('RATIONALE')
        if rationale:
            return rationale
        raise KeyError('The key does not exist within the configuration file.')

    @property
    def impact(self) -> str:
        impact = self._config.get('IMPACT')
        if impact:
            return impact
        raise KeyError('The key does not exist within the configuration file.')

    @property
    def safeguard(self) -> str:
        safeguard = self._config.get('SAFEGUARD')
        if safeguard:
            return safeguard
        raise KeyError('The key does not exist within the configuration file.')

    @property
    def overview_sheet(self) -> str:
        overview_sheet = self._config.get('OVERVIEW_SHEET')
        if overview_sheet:
            return overview_sheet
        raise KeyError('The key does not exist within the configuration file.')

    @property
    def required_columns(self) -> set:
        required_column_titles = set(self._config.get('REQUIRED_COLUMN_TITLES'))
        if required_column_titles:
            return required_column_titles
        raise KeyError('The key does not exist within the configuration file.')

    @property
    def commands_path(self) -> str:
        commands_path = self._config.get('COMMANDS_PATH')
        if commands_path:
            return commands_path
        raise KeyError('The key does not exist within the configuration file.')

    def __repr__(self):
        return f'CISBenchmarksLoadConfig(config_path="{self._config_path}", config_loader="{self._config_loader}")'


class CISBenchmarksLoadWorkbook(ExcelOpenWorkbook):
    def __init__(self, *, workbook_loader: IWorkbookLoader, workbook_path: str):
        self._workbook_path = validate_and_return_file_path(workbook_path, 'xlsx')
        super().__init__(workbook_loader)

    def _load_workbook(self):
        return self._workbook_loader.load(self._workbook_path)


class CISBenchmarksWorkbookValidator(ExcelValidator):
    def __init__(self, workbook):
        super().__init__(workbook)

    @staticmethod
    def validate_column_titles(column_indices: dict, required_columns: set) -> bool:
        columns_to_check = column_indices.keys()
        if not required_columns.issubset(columns_to_check):
            missing_columns = required_columns.difference(columns_to_check)
            raise AttributeError(
                f"The following columns do not exist in the worksheet: '{', '.join(missing_columns)}'.")
        return True

    def validate_and_return_sheet_name(self, sheet_name: str) -> str:
        sheetnames_list = self._workbook.sheetnames
        if sheet_name not in sheetnames_list:
            raise ValueError(f'"{sheet_name}" is not in the sheet names. Possible sheet names: {sheetnames_list}.')
        return sheet_name

    @staticmethod
    def validate_and_return_scope_level(curr_scope_level: int, allowed_scope_levels: set) -> int:
        if not isinstance(curr_scope_level, int):
            raise TypeError(f'scope_level must be an integer, got {type(curr_scope_level).__name__}')
        if curr_scope_level not in allowed_scope_levels:
            raise ValueError(f'{curr_scope_level} is not in the scope levels.')
        return curr_scope_level

    def validate_and_return_benchmark_scope_profile(self, curr_scope_level: int, scope_levels_os_mapping: dict) -> str:
        allowed_scope_levels = set(map(int, scope_levels_os_mapping.keys()))
        scope_level = self.validate_and_return_scope_level(curr_scope_level, allowed_scope_levels)
        scope_level_os = scope_levels_os_mapping.get(scope_level)
        if scope_level_os is None:
            raise ValueError(f'Benchmark profile for level {scope_level} does not exist.')
        return next(iter(scope_level_os))


class CISBenchmarksProcessWorkbook(CISBenchmarksLoadWorkbook):
    def __init__(self, *, workbook_loader: IWorkbookLoader, workbook_path: str,
                 benchmarks_config: CISBenchmarksLoadConfig):
        super().__init__(workbook_loader=workbook_loader, workbook_path=workbook_path)
        self._config = benchmarks_config
        self._excel_validator = CISBenchmarksWorkbookValidator(self._workbook)
        self._scope_levels_os_mapping = self._get_scope_levels_os_mapping()

    def _get_overview_worksheet(self) -> Worksheet:
        sheet_name = self._excel_validator.validate_and_return_sheet_name(self._config.overview_sheet)
        overview_worksheet = self._workbook[sheet_name]
        if not overview_worksheet:
            raise KeyError(f'"{sheet_name}" sheet name cannot be found.')
        return overview_worksheet

    def _get_scope_levels_os_mapping(self) -> Dict:
        overview_worksheet = self._get_overview_worksheet()
        regex_pattern = self._config.benchmark_profiles_rex
        scope_levels_os_mapping = {}
        for row in overview_worksheet.iter_rows(values_only=True):
            for cell in row:
                match = re.search(regex_pattern, str(cell))
                if match:
                    try:
                        os_system, level = match.groups()
                        scope_levels_os_mapping[level] = os_system
                    except (IndexError, ValueError) as e:
                        raise ValueError(f'Invalid data format in cell: {cell}. Error: {e}')
        return scope_levels_os_mapping


json_config_loader = JSONConfigLoader()
openpyxl_workbook_loader = OpenPyXLWorkbookLoader()

cis_benchmarks_config = CISBenchmarksLoadConfig(config_loader=json_config_loader,
                                                config_path='config/cis_workbooks_config.json')
workbook_processor = CISBenchmarksProcessWorkbook(workbook_loader=openpyxl_workbook_loader,
                                                  workbook_path='cis_benchmarks/CIS_Apple_macOS_13.0_Ventura_Benchmark_v2.0.0.1.xlsx',
                                                  benchmarks_config=cis_benchmarks_config)


#
# print(cis_benchmarks_config.required_columns)
# print(cis_benchmarks_workbook._workbook.sheetnames)


# class CISBenchmarkManager(ExcelOpenWorkbook):
#     def __init__(self, *, workbook_path: str, audit_manager: AuditCommandManager, cis_control_manager: CISControlsProcessWorkbook):
#         super().__init__(workbook_path)
#         self._workbook = self.load_workbook()
#         self._config = self.load_config()
#         self._audit_manager = audit_manager
#         self._cis_control_manager = cis_control_manager
#         self._benchmark_profiles = self._get_benchmark_profiles()
#         self._scope_levels_os_mapping = self._populate_scope_levels_os_mapping()
#         self._headers = None
#         self._populate_benchmark_cache_and_headers()
#         self._map_recommendations_and_cis_controls()
#         self._map_recommendations_and_audit_commands()
#
#     def load_workbook(self):
#         return openpyxl.load_workbook(self.workbook_path)
#
#     def load_config(self):
#         try:
#             with open(self.config_path, 'r') as config_file:
#                 return json.load(config_file)[__class__.__name__]
#         except json.JSONDecodeError as e:
#             raise ValueError(f'Error parsing JSON file at {self.config_path}: {e}')
#
#     @property
#     def benchmark_profiles(self) -> List[Tuple]:
#         return self._benchmark_profiles
#
#     @property
#     def scope_levels_os_mapping(self) -> Dict:
#         return self._scope_levels_os_mapping
#
#     @property
#     def scope_levels(self) -> Dict:
#         return {int(level): title for level, title in self._config['SCOPE_LEVELS'].items()}
#
#     @property
#     def allowed_assessment_methods(self) -> Set:
#         return self._config['ALLOWED_ASSESSMENT_METHODS']
#
#     @property
#     def benchmark_profiles_rex(self) -> str:
#         return self._config['BENCHMARK_PROFILES_REX']
#
#     @property
#     def recommendation(self) -> str:
#         return self._config['RECOMMENDATION']
#
#     @property
#     def rationale(self) -> str:
#         return self._config['RATIONALE']
#
#     @property
#     def impact(self) -> str:
#         return self._config['IMPACT']
#
#     @property
#     def assess_status(self) -> str:
#         return self._config['ASSESS_STATUS']
#
#     @property
#     def section(self) -> str:
#         return self._config['SECTION']
#
#     @property
#     def overview_sheet(self) -> str:
#         return self._config['OVERVIEW_SHEET']
#
#     def _get_benchmark_profiles(self) -> list:
#         regex_pattern = self.benchmark_profiles_rex
#         sheet_name = self._validate_and_return_sheet_name(self.overview_sheet)
#         overview_worksheet = self._workbook[sheet_name]
#         overview_paragraphs = str([paragraph for paragraph in overview_worksheet.iter_rows(values_only=True)])
#         return re.findall(regex_pattern, overview_paragraphs)
#
#     def _populate_scope_levels_os_mapping(self) -> Dict:
#         benchmark_profiles = self._benchmark_profiles
#         scope_levels_os_mapping = defaultdict(list)
#         for profile, profile_level in benchmark_profiles:
#             scope_levels_os_mapping[int(profile_level)].append(profile)
#         return scope_levels_os_mapping
#
#     def _validate_and_return_benchmark_scope_profile(self, scope_level: int) -> str:
#         scope_level = self._validate_and_return_scope_level(scope_level)
#         scope_level_os = self._scope_levels_os_mapping[scope_level]
#         if not scope_level_os:
#             raise ValueError(f'Benchmark profile for level {scope_level} does not exist.')
#         return next(iter(scope_level_os))
#
#     def _validate_and_return_scope_level(self, scope_level: int) -> int:
#         if not isinstance(scope_level, int):
#             raise TypeError(f'scope_level must be an integer, got {type(scope_level).__name__}')
#         if scope_level not in self.scope_levels:
#             raise ValueError(f'{scope_level} is not in the scope levels.')
#         return scope_level
#
#     @staticmethod
#     def _validate_and_return_item_id(item_id: str) -> str:
#         if not isinstance(item_id, str):
#             raise TypeError(f'item_id must be a string, got {type(item_id).__name__}')
#         return item_id
#
#     def _validate_and_get_items_by_type(self, scope_level: int, item_type: str) -> List[Recommendation] | List[RecommendHeader]:
#         if item_type.casefold() == 'recommendation':
#             scope_items = self.get_recommendations_by_level(scope_level=scope_level)
#         elif item_type.casefold() == 'recommend_header':
#             scope_items = self.get_recommendations_scope_headers(scope_level=scope_level)
#         else:
#             raise KeyError(
#                 f'Invalid item type "{item_type}" provided. Item types can be either "recommendation" or "recommend_header".')
#         return scope_items
#
#     def _validate_assessment_method_type(self, assessment_method: str) -> str:
#         if assessment_method is None:
#             raise ValueError("Assessment method cannot be 'None'.")
#         if assessment_method.casefold() not in self.allowed_assessment_methods:
#             raise ValueError(
#                 f"{assessment_method} is not in allowed assessment methods. The allowed assessment methods are: '{self.allowed_assessment_methods}'.")
#         return assessment_method
#
#     def _get_worksheet_scope_headers(self, scope_level: int) -> Tuple[Worksheet, Dict[str, int]]:
#         scope_level = self._validate_and_return_scope_level(scope_level)
#         curr_sheet_level = self.scope_levels[scope_level]
#         sheet_name = self._validate_and_return_sheet_name(curr_sheet_level)
#         worksheet = self._workbook[sheet_name]
#         header_row = next(worksheet.iter_rows(min_row=1, max_row=1, values_only=True))
#         column_indices = {title: index for index, title in enumerate(header_row)}
#
#         return worksheet, column_indices
#
#     def _get_worksheet_row_attributes(self, worksheet: Worksheet, column_indices: Dict[str, int]) -> Iterator[Tuple[str, str, str, bool]]:
#         if self._validate_column_titles(column_indices, self.required_column_titles):
#             for row in worksheet.iter_rows(min_row=2, values_only=True):
#                 recommend_id = row[column_indices[self.recommendation]]
#                 title = row[column_indices[self.title]]
#                 description = row[column_indices[self.description]]
#                 rationale = row[column_indices[self.rationale]]
#                 impact = row[column_indices[self.impact]]
#                 safeguard_id = row[column_indices[self.safeguard]]
#                 assessment_method = row[column_indices[self.assess_status]]
#                 is_header = False
#
#                 if not assessment_method:
#                     is_header = True
#                     recommend_id = row[column_indices[self.section]]
#
#                 yield recommend_id, title, description, rationale, impact, safeguard_id, assessment_method, is_header
#
#     def _get_worksheet_all_scopes_row_attributes(self) -> Generator:
#         all_scopes_mapping = self._scope_levels_os_mapping.items()
#         for level, benchmark_profiles in all_scopes_mapping:
#             worksheet, column_indices = self._get_worksheet_scope_headers(level)
#             worksheet_row_attrs = self._get_worksheet_row_attributes(worksheet, column_indices)
#             for profile in benchmark_profiles:
#                 yield level, profile, worksheet_row_attrs
#
#     def _initialize_cache_and_headers_keys(self) -> Tuple[Dict[str, List], Dict[str, List]]:
#         cache_mapping = {}
#         headers_mapping = {}
#         for _, benchmark_profiles in self._scope_levels_os_mapping.items():
#             for profile in benchmark_profiles:
#                 cache_mapping[profile] = []
#                 headers_mapping[profile] = []
#         return cache_mapping, headers_mapping
#
#     def _populate_benchmark_cache_and_headers(self):
#         self._cache, self._headers = self._initialize_cache_and_headers_keys()
#         all_scopes_attributes = self._get_worksheet_all_scopes_row_attributes()
#         for level, profile, worksheet_row_attrs in all_scopes_attributes:
#             for recommend_id, title, description, rationale, impact, safeguard_id, assessment_method, is_header in worksheet_row_attrs:
#                 if is_header:
#                     header = RecommendHeader(recommend_id=recommend_id, level=level, title=title,
#                                              description=description)
#                     self._headers[profile].append(header)
#                 else:
#                     recommendation = Recommendation(recommend_id=recommend_id, level=level, title=title,
#                                                     rationale=rationale,
#                                                     impact=impact, safeguard_id=safeguard_id,
#                                                     assessment_method=assessment_method)
#                     self._cache[profile].append(recommendation)
#
#     def get_item_by_id(self, *, scope_level: int = 1, item_id: str, item_type: str) -> Recommendation | RecommendHeader:
#         scope_level = self._validate_and_return_scope_level(scope_level)
#         item_id = self._validate_and_return_item_id(item_id)
#         scope_items = self._validate_and_get_items_by_type(scope_level, item_type)
#
#         for item in scope_items:
#             if item_id == item.recommend_id:
#                 return item
#
#         raise KeyError(f'{item_type.capitalize()} with ID {item_id} is not in level {scope_level} of {item_type}s.')
#
#     def get_recommendations_by_level(self, *, scope_level: int = 1) -> List[Recommendation]:
#         scope_level = self._validate_and_return_scope_level(scope_level)
#         scope_profile = self._validate_and_return_benchmark_scope_profile(scope_level)
#         return self._cache[scope_profile]
#
#     def get_all_levels_recommendations(self) -> Dict[str, List[Dict[str, Recommendation]]]:
#         return self._cache
#
#     def get_recommendations_scope_headers(self, *, scope_level: int = 1) -> List[RecommendHeader]:
#         scope_level = self._validate_and_return_scope_level(scope_level)
#         scope_profile = self._validate_and_return_benchmark_scope_profile(scope_level)
#         return self._headers[scope_profile]
#
#     def get_all_scopes_recommendation_headers(self) -> Dict[str, List[RecommendHeader]]:
#         return self._headers
#
#     def get_recommendations_by_assessment_method(self, *, scope_level: int = 1, assessment_method: str = None) -> Generator:
#         assessment_method = self._validate_assessment_method_type(assessment_method)
#         recommendations_scope = self.get_recommendations_by_level(scope_level=scope_level)
#         for recommendation in recommendations_scope:
#             if assessment_method == recommendation.assessment_method.casefold():
#                 yield recommendation
#
#     def _map_recommendations_and_cis_controls(self):
#         all_cis_controls = {control.safeguard_id: control for control in self._cis_control_manager.get_all_controls()}
#         for scope_level in self.scope_levels:
#             recommendations_scope = self.get_recommendations_by_level(scope_level=scope_level)
#             for recommendation in recommendations_scope:
#                 control = all_cis_controls.get(recommendation.safeguard_id)
#                 if control:
#                     recommendation.cis_control = control
#
#     def _map_recommendations_and_audit_commands(self):
#         audit_commands = self._audit_manager.audit_commands
#         commands_map = {cmd['recommend_id']: cmd for cmd in audit_commands}
#
#         for scope_level in self.scope_levels:
#             recommendations_scope = self.get_recommendations_by_level(scope_level=scope_level)
#             for recommendation in recommendations_scope:
#                 if recommendation.recommend_id in commands_map:
#                     cmd = commands_map[recommendation.recommend_id]
#                     command, expected_output = self._audit_manager.get_command_attrs(cmd)
#                     recommendation.audit_cmd = AuditCmd(command=command, expected_output=expected_output)
#
#     def evaluate_recommendations_compliance(self, *, scope_level: int = 1) -> List[Recommendation]:
#         recommendations_scope = self.get_recommendations_by_level(scope_level=scope_level)
#         for recommendation in recommendations_scope:
#             audit_cmd = recommendation.audit_cmd
#             if audit_cmd:
#                 command = audit_cmd.command
#                 expected_output = audit_cmd.expected_output
#                 audit_result = self._audit_manager.run_command(command, expected_output)
#                 recommendation.compliant = audit_result
#                 yield recommendation
#
#     def __repr__(self) -> str:
#         return f'CISBenchmarkManager(workbook_path="{self.workbook_path}", config_path="{self.config_path}")'
