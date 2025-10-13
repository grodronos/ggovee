# GoveeApi/DeviceState/models/response.py
from dataclasses import dataclass
from typing import Any, Dict
from .payload import Payload


@dataclass
class Response:
    requestId: str
    msg: str
    code: int
    payload: Payload

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Response":
        return cls(
            requestId=data.get("requestId", ""),
            msg=data.get("msg", ""),
            code=data.get("code", 0),
            payload=Payload.from_dict(data.get("payload", {})),
        )
