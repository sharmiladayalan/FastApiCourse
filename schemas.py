from pydantic import BaseModel, Field
from enum import Enum



class ShipmentStatus(str, Enum):
    placed = "Placed"
    in_transit = "In transit"
    out_for_delivery = "Out for delivery"
    delivered = "Delivered"
    pending = "Pending"



class BaseShipment(BaseModel):
    id: int
    weight: float = Field(le=25)
    content: str =Field(max_length=70)
    distination: int
   

class ShipmentRead(BaseShipment):
    id: int
    status: ShipmentStatus


class Order(BaseModel):   
    price: int
    title: str
    description: str

class ShipmentCreate(BaseShipment):
    order: Order
    pass

class ShipmentUpdate(BaseModel):
    id: int
    status: ShipmentStatus