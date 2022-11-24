from pydantic import BaseModel
from typing import Any, Union


class Item(BaseModel):
    where: Union[dict, None] = None


class Station(BaseModel):
    stationId: int


class ResponseModel(BaseModel):
    id: int
    harvestTimeUtc: Union[str, None] = None
    stationId: int
    availableBikeStands: int
    bikeStands: int
    availableBikes: int
    banking: str
    bonus: bool
    lastUpdate: str
    status: str
    address: str
    name: str
    latitude: Union[float, None] = None
    longitude: Union[float, None] = None


class Field(BaseModel):
    display: str = None
    name: str = None
    type: Any = None
    options: list = None
