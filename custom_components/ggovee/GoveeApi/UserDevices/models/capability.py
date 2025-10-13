# models/capability.py
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Capability:
    type: str
    instance: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Capability":
        return cls(
            type=data.get("type", ""),
            instance=data.get("instance", ""),
        )
