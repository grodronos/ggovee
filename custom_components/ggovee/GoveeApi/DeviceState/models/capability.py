# GoveeApi/DeviceState/models/capability.py
from dataclasses import dataclass
from typing import Any, Dict
from .state import State


@dataclass
class Capability:
    type: str
    instance: str
    state: State

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Capability":
        return cls(
            type=data.get("type", ""),
            instance=data.get("instance", ""),
            state=State.from_dict(data.get("state")),
        )
