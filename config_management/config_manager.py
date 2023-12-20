from abc import ABC, abstractmethod
from config_management.interfaces import IConfigLoader


class OpenConfig(ABC):
    def __init__(self, config_loader: IConfigLoader):
        self._config_loader = config_loader
        self._config = self._load_config()

    @abstractmethod
    def _load_config(self):
        pass


class ControlsConfigAttrs(OpenConfig):
    @property
    @abstractmethod
    def worksheet_name(self) -> str:
        pass

    @property
    @abstractmethod
    def cis_safeguard(self) -> str:
        pass

    @property
    @abstractmethod
    def control_family_id(self) -> str:
        pass

    @property
    @abstractmethod
    def asset_type(self) -> str:
        pass

    @property
    @abstractmethod
    def domain(self) -> str:
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def required_columns(self) -> set:
        pass


class BenchmarksConfigAttrs(OpenConfig):
    @property
    @abstractmethod
    def allowed_scope_levels(self) -> dict:
        pass

    @property
    @abstractmethod
    def allowed_assessment_methods(self) -> list:
        pass

    @property
    @abstractmethod
    def benchmark_profiles_rex(self) -> str:
        pass

    @property
    @abstractmethod
    def section(self) -> str:
        pass

    @property
    @abstractmethod
    def recommendation(self) -> str:
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def assessment_status(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def rationale(self) -> str:
        pass

    @property
    @abstractmethod
    def impact(self) -> str:
        pass

    @property
    @abstractmethod
    def safeguard(self) -> str:
        pass

    @property
    @abstractmethod
    def overview_sheet(self) -> str:
        pass

    @property
    @abstractmethod
    def required_columns(self) -> set:
        pass

    @property
    @abstractmethod
    def commands_path(self) -> str:
        pass


class AuditAttrs(OpenConfig):
    @property
    @abstractmethod
    def os_version_rex(self) -> str:
        pass

    @property
    @abstractmethod
    def os_versions_mapping(self) -> dict:
        pass

    @property
    @abstractmethod
    def allowed_os_versions(self) -> list:
        pass
