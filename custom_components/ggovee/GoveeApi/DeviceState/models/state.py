# GoveeApi/DeviceState/models/state.py
from dataclasses import dataclass
from typing import Any, Dict, Union


@dataclass
class State:
    value: Union[bool, float, Dict[str, int], Any]

    @classmethod
    def from_dict(cls, data: Any) -> "State":
        if isinstance(data, dict) and "value" in data:
            return cls(value=data.get("value"))
        return cls(value=data)
