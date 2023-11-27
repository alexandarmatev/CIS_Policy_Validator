from utils.validation_utils import validate_and_return_file_path, cmd_output_validate_and_return
from utils.config_load_utils import load_config
import subprocess
import re


class AuditCommands:
    def __init__(self, config_path):
        self._config_path = validate_and_return_file_path(config_path, 'json')
        self._config = load_config(config_path)[self.__class__.__name__]
        self._all_commands = {'MacOS Ventura': [], 'MacOS Sonoma': []}

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

    def get_current_os_version(self) -> str:
        try:
            cmd_result = subprocess.run('sw_vers', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            cmd_stdout = cmd_output_validate_and_return(cmd_result)[1]
            match = re.findall(self.os_version_rex, cmd_stdout)

            if not match:
                raise ValueError(f"OS version regex match failed. Regex pattern: '{self.os_version_rex}'")

            rex_os = match[0]
            os_version = self.os_mapping[rex_os]

            if os_version not in self.allowed_os_versions:
                raise ValueError(f"{os_version} cannot be audited. Auditable OS versions are: {', '.join(self.allowed_os_versions)}")

            return os_version

        except (RuntimeError, ValueError, IndexError, KeyError) as error:
            print(f"Error occurred: '{error}'.")


audit = AuditCommands('config/cis_workbooks_config.json')
print(audit.config)
print(audit.os_version_rex)
print(audit.os_mapping)
print(audit.get_current_os_version())
