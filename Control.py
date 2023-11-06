from dataclasses import dataclass


@dataclass
class Control:
    control_id: int
    title: str
    description: str
    level: int
    header: bool
    audit_cmd: str = None
