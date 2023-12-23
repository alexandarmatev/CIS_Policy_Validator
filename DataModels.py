from dataclasses import dataclass
from utils.validation_utils import data_type_validator


# @dataclass(kw_only=True, frozen=True)
# class AuditCmd:
#     """
#     Represents an audit command with its expected output.
#
#     Attributes:
#         command: The audit command to be executed.
#         expected_output: The expected output of the audit command.
#     """
#     command: str
#     expected_output: str
#
#     def __post_init__(self):
#         """
#         Validates the data types of the attributes on instantiation.
#         """
#         for attr_name, attr_type in self.__annotations__.items():
#             attr_value = getattr(self, attr_name)
#             data_type_validator(attr_name, attr_value, attr_type)


@dataclass(kw_only=True, frozen=True)
class CISControl:
    """
    Represents a CIS control with its attributes.

    Attributes:
        safeguard_id: Identifier for the safeguard.
        asset_type: Type of the asset.
        domain: Domain of the CIS control.
        title: Title of the CIS control.
        description: Description of the CIS control.
    """
    safeguard_id: str
    asset_type: str
    domain: str
    title: str
    description: str

    def __post_init__(self):
        """
        Validates the data types of the attributes on instantiation.
        """
        for attr_name, attr_type in self.__annotations__.items():
            attr_value = getattr(self, attr_name)
            data_type_validator(attr_name, attr_value, attr_type)


@dataclass(kw_only=True)
class Recommendation:
    """
    Represents a recommendation with its details and associated CIS control and audit command.

    Attributes:
        recommend_id: Identifier for the recommendation.
        level: Level of the recommendation.
        title: Title of the recommendation.
        rationale: Rationale behind the recommendation.
        impact: Impact of the recommendation.
        safeguard_id: Associated safeguard identifier.
        assessment_method: Method of assessment for the recommendation.
        cis_control: Associated CIS Control object (optional).
        audit_cmd: Associated AuditCmd object (optional).
        compliant: Compliance status (optional).
    """
    recommend_id: str
    level: int
    title: str
    rationale: str
    impact: str
    safeguard_id: str
    assessment_method: str
    cis_control: CISControl = None
    audit_cmd: dict = None
    compliant: str = None

    def __post_init__(self):
        """
        Validates the data types of the attributes on instantiation.
        """
        for attr_name, attr_type in self.__annotations__.items():
            attr_value = getattr(self, attr_name)
            data_type_validator(attr_name, attr_value, attr_type)


@dataclass(kw_only=True, frozen=True)
class RecommendHeader:
    """
    Represents the header information for a recommendation.

    Attributes:
        recommend_id: Identifier for the recommendation.
        level: Level of the recommendation.
        title: Title of the recommendation.
        description: Description of the recommendation.
    """
    recommend_id: str
    level: int
    title: str
    description: str

    def __post_init__(self):
        """
        Validates the data types of the attributes on instantiation.
        """
        for attr_name, attr_type in self.__annotations__.items():
            attr_value = getattr(self, attr_name)
            data_type_validator(attr_name, attr_value, attr_type)


@dataclass(kw_only=True, frozen=True)
class CISControlFamily:
    """
    Represents a CIS control family with its title and description.

    Attributes:
        title: Title of the CIS control family.
        description: Description of the CIS control family.
    """
    title: str
    description: str

    def __post_init__(self):
        """
        Validates the data types of the attributes on instantiation.
        """
        for attr_name, attr_type in self.__annotations__.items():
            attr_value = getattr(self, attr_name)
            data_type_validator(attr_name, attr_value, attr_type)



