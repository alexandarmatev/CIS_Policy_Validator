from dataclasses import dataclass


def _type_validator(attr_name, attr_value, attr_type):
    if attr_value and not isinstance(attr_value, attr_type):
        raise TypeError(f'Provided argument "{attr_value}" to {attr_name} must be of type {attr_type.__name__}.')


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
            _type_validator(attr_name, attr_value, attr_type)


@dataclass(kw_only=True, frozen=True)
class RecommendHeader:
    header_id: str
    level: int
    title: str
    description: str

    def __post_init__(self):
        for attr_name, attr_type in self.__annotations__.items():
            attr_value = getattr(self, attr_name)
            _type_validator(attr_name, attr_value, attr_type)


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
            _type_validator(attr_name, attr_value, attr_type)


