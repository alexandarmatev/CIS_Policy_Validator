from typing import List, Dict, Tuple
from utils.validation_utils import validate_and_return_file_path, validate_and_return_os_version, validate_and_return_workbook_version_path
from utils.config_load_utils import load_config
import subprocess
import re


class AuditCommandManager:
    """
    AuditCommandManager is responsible for managing audit commands based on operating system versions.
    It facilitates the execution and evaluation of audit commands.

    Attributes:
        _config_path (str): Path to the JSON configuration file.
        _commands_path (str): Path to the JSON file containing audit commands.
        _config (dict): Configuration data specific to the class instance.
        _os_version (str): Operating system version for which the audit commands are applicable.
        _workbook_version_path (str): Path to the workbook file version specific to the OS version.
        _audit_commands (List[Dict]): List of audit command dictionaries specific to the OS version.
    """
    def __init__(self, config_path, commands_path, *, os_version=None):
        """
        Initializes the AuditCommandManager with configuration and commands paths.
        It loads configuration and audit commands specific to the given or current OS version.

        Parameters:
            config_path: Path to the JSON configuration file.
            commands_path: Path to the JSON file containing audit commands.
            os_version: Optional; specific OS version to use. If not provided, the current OS version is used.
        """
        self._config_path = validate_and_return_file_path(config_path, 'json')
        self._commands_path = validate_and_return_file_path(commands_path, 'json')
        self._config = load_config(config_path)[self.__class__.__name__]
        if os_version is None:
            self._os_version = validate_and_return_os_version(self._get_current_os_version(), self.allowed_os_versions)
        else:
            self._os_version = validate_and_return_os_version(os_version, self.allowed_os_versions)
        self._workbook_version_path = validate_and_return_workbook_version_path(self.os_version)
        self._audit_commands = load_config(commands_path)[self.os_version]

    @property
    def config(self) -> dict:
        """
        Gets the configuration data specific to the class instance.

        Returns:
            The configuration data.
        """
        return self._config

    @property
    def config_path(self) -> str:
        """
        Gets the path to the JSON configuration file.

        Returns:
            The path to the configuration file.
        """
        return self._config_path

    @property
    def commands_path(self) -> str:
        """
        Gets the path to the JSON file containing audit commands.

        Returns:
            The path to the audit commands file.
        """
        return self._commands_path

    @property
    def workbook_path(self) -> str:
        """
        Gets the path to the workbook file version specific to the OS version.

        Returns:
            The path to the workbook file.
        """
        return self._workbook_version_path

    @property
    def audit_commands(self) -> List[Dict]:
        """
        Gets the audit commands specific to the OS version.

        Returns:
            A list of audit commands.

        Raises:
            ValueError: If audit commands are not found.
        """
        if len(self._audit_commands[0]) > 0:
            return self._audit_commands
        raise ValueError('Audit commands not found.')

    @property
    def os_version(self) -> str:
        """
        Gets the operating system version.

        Returns:
            The OS version.
        """
        return self._os_version

    @property
    def os_version_rex(self) -> str:
        """
        Gets the regular expression used for extracting the OS version.

        Returns:
            A string representing the regular expression for the OS version.
        """
        return self.config['OS_VERSION_REX']

    @property
    def os_mapping(self) -> Dict[str, str]:
        """
        Gets the mapping for OS versions.

        Returns:
            A dictionary mapping OS version strings to their respective standardized representations.
        """
        return self.config['OS_MAPPING']

    @property
    def allowed_os_versions(self) -> List[str]:
        """
        Gets the list of allowed operating system versions.

        Returns:
            A list of allowed OS versions.
        """
        return self.config['ALLOWED_OS_VERSIONS']

    def _get_current_os_version(self) -> str:
        """
        Determines the current operating system version.

        Returns:
            The current OS version.

        Raises:
            Various exceptions if there are issues in determining the OS version.
        """
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
        """
        Executes a given shell command and captures its output and return code.

        Parameters:
            command: The shell command to be executed.

        Returns:
            Tuple containing a list of lines from standard output, a list of lines from standard error, and the command's return code.
        """
        audit_cmd = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout = audit_cmd.stdout.decode('UTF-8').split('\n')
        stderr = audit_cmd.stderr.decode('UTF-8').split('\n')
        return_code = audit_cmd.returncode
        return stdout, stderr, return_code

    @staticmethod
    def get_command_attrs(audit_command: dict) -> Tuple:
        """
        Extracts the command string and expected output from an audit command dictionary.

        Parameters:
            audit_command: A dictionary representing an audit command, containing keys for 'command' and 'expected_output'.

        Returns:
            Tuple containing the command string and the expected output string.
        """
        command = audit_command['command']
        expected_output = audit_command['expected_output']
        return command, expected_output

    def run_command(self, audit_cmd: str, expected_output: str) -> str | bool:
        """
        Runs an audit command and checks if the expected output is in the command's standard output.

        Parameters:
            audit_cmd: The audit command to be executed.
            expected_output: The expected output string for the command.

        Returns:
            A boolean indicating whether the expected output is in the standard output, or an error string if the command fails.
        """
        stdout, stderr, return_code = self._shell_exec(audit_cmd)
        stdout = [output.strip() for output in stdout if output]
        if return_code != 0 and stderr[0]:
            return stderr[0]
        return expected_output in stdout











