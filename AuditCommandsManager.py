from typing import List, Dict, Tuple
from utils.validation_utils import validate_and_return_file_path, validate_and_return_os_version, validate_and_return_workbook_version_path
from utils.config_load_utils import load_config
import subprocess
import re


class AuditCommandsManager:
    def __init__(self, config_path, commands_path, *, os_version=None):
        self._config_path = validate_and_return_file_path(config_path, 'json')
        self._commands_path = commands_path
        self._config = load_config(config_path)[self.__class__.__name__]
        if os_version is None:
            self._os_version = validate_and_return_os_version(self._get_current_os_version(), self.allowed_os_versions)
        else:
            self._os_version = validate_and_return_os_version(os_version, self.allowed_os_versions)
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
        return self._audit_commands

    @property
    def os_version(self) -> str:
        return self._os_version

    @property
    def os_version_rex(self) -> str:
        return self.config['OS_VERSION_REX']

    @property
    def os_mapping(self) -> dict:
        return self.config['OS_MAPPING']

    @property
    def allowed_os_versions(self) -> list:
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
    def _shell_exec(command: str):
        audit_cmd = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout = audit_cmd.stdout.decode('UTF-8').split('\n')
        stderr = audit_cmd.stderr.decode('UTF-8').split('\n')
        return_code = audit_cmd.returncode
        return stdout, stderr, return_code

    @staticmethod
    def _get_command_attrs(audit_command: dict) -> Tuple:
        recommend_id = audit_command['recommend_id']
        description = audit_command['description']
        command = audit_command['command']
        expected_output = audit_command['expected_output']
        return recommend_id, description, command, expected_output

    def run_commands(self):
        for audit_command in self.audit_commands:
            recommend_id, description, command, expected_output = self._get_command_attrs(audit_command)
            stdout, stderr, return_code = self._shell_exec(command)
            stdout = [output.strip() for output in stdout if output]

            if return_code != 0 and stderr[0]:
                print(stderr[0])
            if expected_output in stdout:
                print(f'{description}: Compliant')
            else:
                print(f'{description}: Not Compliant')

    def run_command(self, audit_cmd, expected_output):
        # description, recommend_id, command, expected_output = self._get_command_attrs(audit_cmd)
        stdout, stderr, return_code = self._shell_exec(audit_cmd)
        stdout = [output.strip() for output in stdout if output]
        if return_code != 0 and stderr[0]:
            print(stderr[0])
        if expected_output in stdout:
            print('Compliant')
        else:
            print('Not Compliant')










