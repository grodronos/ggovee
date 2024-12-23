# GoveeApi/DeviceState/models/capability.py
from pydantic import BaseModel
from .state import State


class Capability(BaseModel):
    type: str
    instance: str
    state: State
