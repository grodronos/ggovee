# models/device.py
from dataclasses import dataclass, field
from typing import Any, Dict, List
from .capability import Capability


@dataclass
class Device:
    sku: str
    device: str
    deviceName: str
    type: str
    capabilities: List[Capability] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Device":
        capabilities = [
            Capability.from_dict(item) for item in data.get("capabilities", [])
        ]
        return cls(
            sku=data.get("sku", ""),
            device=data.get("device", ""),
            deviceName=data.get("deviceName", ""),
            type=data.get("type", ""),
            capabilities=capabilities,
        )
