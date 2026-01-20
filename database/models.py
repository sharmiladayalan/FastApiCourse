# First we need to install sqlmodel package
# pip install sqlmodel

# SQLModel is used here instead of Pydantic BaseModel for Object relational mapping(ORM) capabilities
# Here we define the Shipment model that maps to a database table
# and variables are defined as columns in that table
# We can also use constraints like max length and less than or equal to

import datetime
from sqlmodel import SQLModel, Field
from enum import Enum

class ShipmentStatus(str, Enum):
    placed = "Placed"
    in_transit = "In transit"
    out_for_delivery = "Out for delivery"
    delivered = "Delivered"
    pending = "Pending"


class Shipment(SQLModel):
    # __table__ attribute specifies the name of the table in the database
    __tablename__ = "shipment"
    id: int = Field(Primary_key=True)
    content: str
    weight: float =Field(le=25)
    destination: str
    status: ShipmentStatus
    estimated_delivary: datetime

