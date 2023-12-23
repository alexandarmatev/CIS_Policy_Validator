from typing import List, Dict, Tuple
from DataModels import Recommendation
from config_management.interfaces import IConfigLoader
from utils.validation_utils import validate_and_return_file_path
from config_management.config_manager import AuditAttrs, OpenCommands
from enum import Enum
import subprocess
from workbook_management.workbook_manager import AuditValidator


class CISAuditConst(Enum):
    CIS_AUDIT_CONFIG = 'CISAuditConfig'


class CISAuditLoadConfig(AuditAttrs):
    def __init__(self, *, config_path: str, config_loader: IConfigLoader):
        self._config_path = validate_and_return_file_path(config_path, 'json')
        self._config_title = CISAuditConst.CIS_AUDIT_CONFIG.value
        super().__init__(config_loader)

    def _load_config(self) -> Dict:
        config = self._config_loader.load(self._config_path).get(self._config_title)
        if not config:
            raise KeyError('This configuration does not exist within the configuration file.')
        return config

    @property
    def os_version_rex(self) -> str:
        os_version_rex = self._config.get('OS_VERSION_REX')
        if not os_version_rex:
            raise KeyError('The key does not exist within the configuration file.')
        return os_version_rex

    @property
    def os_versions_mapping(self) -> Dict:
        os_versions_mapping = self._config.get('OS_VERSIONS_MAPPING')
        if not os_versions_mapping:
            raise KeyError('The key does not exist within the configuration file.')
        return os_versions_mapping

    @property
    def allowed_os_versions(self) -> List:
        allowed_os_versions = self._config.get('ALLOWED_OS_VERSIONS')
        if not allowed_os_versions:
            raise KeyError('The key does not exist within the configuration file.')
        return allowed_os_versions

    @property
    def workbooks_os_mapping(self) -> Dict:
        workbooks_os_mapping = self._config.get('WORKBOOKS_OS_MAPPING')
        if not workbooks_os_mapping:
            raise KeyError('The key does not exist within the configuration file.')
        return workbooks_os_mapping

    @property
    def audit_commands_path(self) -> str:
        audit_command_path = self._config.get('AUDIT_COMMANDS_PATH')
        if not audit_command_path:
            raise KeyError('The key does not exist within the configuration file.')
        return audit_command_path

    def __repr__(self):
        return f'CISAuditLoadConfig(config_path="{self._config_path}", config_loader="{self._config_loader}")'


class CISAuditLoadCommands(OpenCommands):
    def __init__(self, *, commands_path: str, commands_loader: IConfigLoader):
        self._commands_path = validate_and_return_file_path(commands_path, 'json')
        super().__init__(commands_loader)

    def _load_commands(self) -> Dict:
        all_commands = self._commands_loader.load(self._commands_path)
        if not all_commands:
            raise KeyError('No commands found.')
        return all_commands

    @property
    def all_audit_commands(self) -> List:
        return self._all_commands

    def get_os_specific_commands(self, os_version: str):
        os_specific_commands = self._all_commands.get(os_version)
        if not os_specific_commands:
            raise ValueError(f'Audit commands for OS version {os_version} not found.')
        return os_specific_commands


class CISAuditValidator(AuditValidator):
    @staticmethod
    def validate_and_return_audit_cmd_attrs(audit_cmd: Dict) -> Tuple[str, str | bool]:
        if not audit_cmd:
            raise ValueError('Invalid audit command provided.')
        command = audit_cmd.get('command')
        if not command:
            raise ValueError(f"Audit command for recommend id '{audit_cmd['recommend_id']}' does not exist.")
        expected_output = audit_cmd.get('expected_output')
        if not expected_output:
            raise ValueError(f"Expected output for recommend id '{audit_cmd['recommend_id']}' does not exist.")
        return command, expected_output


class CISAuditRunner:
    def __init__(self):
        self._validator = CISAuditValidator()

    @staticmethod
    def _shell_exec(command: str) -> Tuple[List[str], List[str], int]:
        audit_cmd = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout = audit_cmd.stdout.decode('UTF-8').split('\n')
        stderr = audit_cmd.stderr.decode('UTF-8').split('\n')
        return_code = audit_cmd.returncode
        return stdout, stderr, return_code

    def _get_command_attrs(self, audit_cmd: Dict) -> Tuple:
        command, expected_output = self._validator.validate_and_return_audit_cmd_attrs(audit_cmd)
        return command, expected_output

    def run_command(self, audit_cmd: Dict) -> str | bool:
        command, expected_output = self._get_command_attrs(audit_cmd)
        stdout, stderr, return_code = self._shell_exec(command)
        stdout = [output.strip() for output in stdout if output]
        if return_code != 0 and stderr[0]:
            return stderr[0]
        return expected_output in stdout

    def evaluate_recommendations_compliance(self, *, recommendations: List) -> List[Recommendation]:
        for recommendation in recommendations:
            audit_cmd = recommendation.audit_cmd
            if audit_cmd:
                audit_result = self.run_command(audit_cmd)
                recommendation.compliant = audit_result
                yield recommendation








