from dataclasses import dataclass
from utils.validation_utils import data_type_validator


@dataclass(kw_only=True)
class Recommendation:
    recommend_id: str
    level: int
    title: str
    rationale: str
    impact: str
    safeguard_id: str
    assessment_method: str
    audit_cmd: str = None

    def __post_init__(self):
        for attr_name, attr_type in self.__annotations__.items():
            attr_value = getattr(self, attr_name)
            data_type_validator(attr_name, attr_value, attr_type)


@dataclass(kw_only=True, frozen=True)
class RecommendHeader:
    header_id: str
    level: int
    title: str
    description: str

    def __post_init__(self):
        for attr_name, attr_type in self.__annotations__.items():
            attr_value = getattr(self, attr_name)
            data_type_validator(attr_name, attr_value, attr_type)


@dataclass(kw_only=True, frozen=True)
class CISControl:
    safeguard_id: str
    asset_type: str
    domain: str
    title: str
    description: str

    def __post_init__(self):
        for attr_name, attr_type in self.__annotations__.items():
            attr_value = getattr(self, attr_name)
            data_type_validator(attr_name, attr_value, attr_type)


@dataclass(kw_only=True, frozen=True)
class CISControlFamily:
    title: str
    description: str

    def __post_init__(self):
        for attr_name, attr_type in self.__annotations__.items():
            attr_value = getattr(self, attr_name)
            data_type_validator(attr_name, attr_value, attr_type)



