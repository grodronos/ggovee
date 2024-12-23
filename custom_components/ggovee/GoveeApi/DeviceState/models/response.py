# GoveeApi/DeviceState/models/response.py
from pydantic import BaseModel, Field
from .payload import Payload


class Response(BaseModel):
    requestId: str = Field(..., alias="requestId")
    msg: str
    code: int
    payload: Payload

    class Config:
        allow_population_by_field_name = True
