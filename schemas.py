from pydantic import BaseModel, Field
from enum import Enum

class ShipmentStatus(Enum):
    placed = "Placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered= "delivered"


class BaseShipment(BaseModel):
    weight: float = Field(le=25)
    content: str =Field(max_length=70)
    distination: int
    status: ShipmentStatus

class ShipmentRead(BaseShipment):
    pass

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus