# GoveeApi/DeviceState/models/payload.py
from dataclasses import dataclass, field
from typing import Any, Dict, List
from .capability import Capability


@dataclass
class Payload:
    sku: str
    device: str
    capabilities: List[Capability] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Payload":
        capabilities = [
            Capability.from_dict(item) for item in data.get("capabilities", [])
        ]
        return cls(
            sku=data.get("sku", ""),
            device=data.get("device", ""),
            capabilities=capabilities,
        )
