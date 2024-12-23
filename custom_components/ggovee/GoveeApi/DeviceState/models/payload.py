# GoveeApi/DeviceState/models/payload.py
from pydantic import BaseModel
from typing import List
from .capability import Capability


class Payload(BaseModel):
    sku: str
    device: str
    capabilities: List[Capability]
