from typing import List, Dict, Tuple
from config_management.interfaces import IConfigLoader
from utils.validation_utils import validate_and_return_file_path
from config_management.config_manager import AuditAttrs, OpenCommands
from workbook_management.workbook_manager import AuditValidator
from enum import Enum
import subprocess
import re


class CISAuditConst(Enum):
    CIS_AUDIT_CONFIG = 'CISAuditConfig'


class CISAuditLoadConfig(AuditAttrs):
    def __init__(self, *, config_path: str, config_loader: IConfigLoader):
        self._config_path = validate_and_return_file_path(config_path, 'json')
        self._config_title = CISAuditConst.CIS_AUDIT_CONFIG.value
        super().__init__(config_loader)

    def _load_config(self) -> dict:
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
    def os_versions_mapping(self) -> dict:
        os_versions_mapping = self._config.get('OS_VERSIONS_MAPPING')
        if not os_versions_mapping:
            raise KeyError('The key does not exist within the configuration file.')
        return os_versions_mapping

    @property
    def allowed_os_versions(self) -> list:
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
    def __init__(self, commands_path: str, os_version: str, config_loader: IConfigLoader):
        self._commands_path = validate_and_return_file_path(commands_path, 'json')
        super().__init__(os_version, config_loader)

    def _load_commands(self, os_version: str) -> dict:
        commands = self._config_loader.load(self._commands_path).get(os_version)
        if not commands:
            raise KeyError(f'The commands for "{os_version}" do not exist within the configuration file.')
        return commands

    @property
    def all_audit_commands(self):
        if not self._commands:
            raise KeyError('Audit commands are not available.')
        return self._commands


class CISAuditValidator(AuditValidator):
    pass


class AuditCommandManager:
    def __init__(self, *, config_path: str, commands_path: str):
        self._config_path = validate_and_return_file_path(config_path, 'json')
        self._commands_path = validate_and_return_file_path(commands_path, 'json')
        self._config = load_config(config_path)[self.__class__.__name__]
        self._os_version = validate_and_return_os_version(self._get_current_os_version(), self.allowed_os_versions)
        self._workbook_version_path = validate_and_return_workbook_version_path(self.os_version)
        self._audit_commands = load_config(commands_path)[self.os_version]

    @property
    def config(self) -> dict:
        return self._config

    @property
    def config_path(self) -> str:
        return self._config_path

    @property
    def commands_path(self) -> str:
        return self._commands_path

    @property
    def workbook_path(self) -> str:
        return self._workbook_version_path

    @property
    def audit_commands(self) -> List[Dict]:
        if len(self._audit_commands[0]) > 0:
            return self._audit_commands
        raise ValueError(f'Audit commands for {self.os_version} not found.')

    @property
    def os_version(self) -> str:
        return self._os_version

    @property
    def os_version_rex(self) -> str:
        return self.config['OS_VERSION_REX']

    @property
    def os_mapping(self) -> Dict[str, str]:
        return self.config['OS_MAPPING']

    @property
    def allowed_os_versions(self) -> List[str]:
        return self.config['ALLOWED_OS_VERSIONS']

    def _get_current_os_version(self) -> str:
        try:
            stdout, stderr, return_code = self._shell_exec('sw_vers')
            if return_code != 0:
                return stderr[0]

            match = re.findall(self.os_version_rex, stdout[1])
            if not match:
                raise ValueError(f"OS version regex match failed. Regex pattern: '{self.os_version_rex}'")

            rex_os = match[0]
            os_version = self.os_mapping[rex_os]

            return os_version

        except (RuntimeError, ValueError, IndexError, KeyError) as error:
            print(f"Error occurred: '{error}'.")

    @staticmethod
    def _shell_exec(command: str) -> Tuple[List[str], List[str], int]:
        audit_cmd = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout = audit_cmd.stdout.decode('UTF-8').split('\n')
        stderr = audit_cmd.stderr.decode('UTF-8').split('\n')
        return_code = audit_cmd.returncode
        return stdout, stderr, return_code

    @staticmethod
    def get_command_attrs(audit_command: dict) -> Tuple:
        command = audit_command['command']
        expected_output = audit_command['expected_output']
        return command, expected_output

    def run_command(self, audit_cmd: str, expected_output: str) -> str | bool:
        stdout, stderr, return_code = self._shell_exec(audit_cmd)
        stdout = [output.strip() for output in stdout if output]
        if return_code != 0 and stderr[0]:
            return stderr[0]
        return expected_output in stdout











