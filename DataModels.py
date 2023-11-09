from dataclasses import dataclass


@dataclass
class Control:
    control_id: int
    title: str
    description: str
    level: int
    audit_cmd: str = None


@dataclass
class Header:
    header_id: int
    title: str
    description: str
    level: int
