# GoveeApi/DeviceState/models/state.py
from typing import Union, Dict
from pydantic import BaseModel


class State(BaseModel):
    value: Union[bool, float, Dict[str, int]]
