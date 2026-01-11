from pydantic import BaseModel, Field
class Shipment(BaseModel):
    weight: float = Field(le=25)
    content: str =Field(max_length=70)
    distination: int
    status: str
