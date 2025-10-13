# models/response.py
from dataclasses import dataclass, field
from typing import Any, Dict, List
from .device import Device


@dataclass
class Response:
    code: int
    message: str
    data: List[Device] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Response":
        devices = [Device.from_dict(item) for item in data.get("data", [])]
        return cls(
            code=data.get("code", 0),
            message=data.get("message", ""),
            data=devices,
        )
