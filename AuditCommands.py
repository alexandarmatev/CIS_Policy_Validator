from utils.validation_utils import validate_and_return_file_path
from utils.config_load_utils import load_config
from DataModels import AuditCommand
import subprocess
import re


class AuditCommands:
    def __init__(self, config_path):
        self._config_path = validate_and_return_file_path(config_path, 'json')
        self._config = load_config(config_path)[self.__class__.__name__]
        self._all_audit_commands = []

    @property
    def config(self) -> dict:
        return self._config

    @property
    def config_path(self) -> str:
        return self._config_path

    @property
    def os_version_rex(self) -> str:
        return self.config['OS_VERSION_REX']

    @property
    def os_mapping(self) -> dict:
        return self.config['OS_MAPPING']

    @property
    def allowed_os_versions(self) -> list:
        return self.config['ALLOWED_OS_VERSIONS']

    @property
    def all_audit_commands(self) -> list[AuditCommand]:
        return self._all_audit_commands

    @staticmethod
    def _shell_exec(command: list[str]):
        audit_cmd = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = audit_cmd.stdout.decode('UTF-8').split('\n')
        stderr = audit_cmd.stderr.decode('UTF-8').split('\n')
        return_code = audit_cmd.returncode
        return stdout, stderr, return_code

    def get_current_os_version(self) -> str:
        try:
            stdout, stderr, return_code = self._shell_exec(['sw_vers'])
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

    def _ensure_all_apple_software_is_current(self):
        stdout, stderr, return_code = self._shell_exec(['/usr/bin/sudo', '/usr/sbin/softwareupdate', '-l'])
        if return_code != 0:
            return stderr[0]
        return stdout

    def _add_cmd(self):
        audit_cmd = AuditCommand(safeguard_id='1.1', function=self._ensure_all_apple_software_is_current, cmd_output=None)
        self._all_audit_commands.append(audit_cmd)
