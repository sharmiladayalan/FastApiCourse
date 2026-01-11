# What is Pydantic?

# Pydantic is a data-validation and data-parsing library used by FastAPI to:

# Define the structure of request data

# Validate incoming data automatically

# Convert data into correct Python types

# FastAPI internally depends on Pydantic for handling request bodies.

# Observing Your Two Codes
# 🔹 Code 1 Using Pydantic (POST /shipment)
# @app.post("/shipment")
# def submit_shipment(shipment: Shipment) -> dict[str, Any]:


# ✔ Data comes as request body (JSON)
# ✔ Structure is defined using Shipment model
# ✔ Automatic validation
# ✔ Clean and scalable

# 🔹 Code 2 – Without Pydantic (PUT /shipment)
# @app.put("/shipment")
# def add_data(id: int, weight: float, content: str, shipment_status: str):


# ❌ Data comes as query parameters
# ❌ No single object representation
# ❌ Harder to scale
# ❌ Poor API design for real-time systems

from enum import Enum
from fastapi import FastAPI
from schemas import Shipment
from typing import Any
app = FastAPI()
shipments ={
    1223:{
    "weight" : 5.8,
    "content" : "Wooden table",
    "status"  : "In transit"
    },
    1224:{
    "weight" : 3.2,
    "content" : "Metal chair",
    "status"  : "Delivered"
    },
    1225:{
    "weight" : 12.5,
    "content" : "Glass bookshelf",
    "status"  : "In transit"
    },
    1226:{
    "weight" : 8.7,
    "content" : "Wooden desk",
    "status"  : "Pending"
    },
    1227:{
    "weight" : 2.1,
    "content" : "Lamp",
    "status"  : "Delivered"
    },
    1228:{
    "weight" : 6.4,
    "content" : "Sofa",
    "status"  : "In transit"
    }
}

@app.get("/shipments")
def get_all_shipment():
    return shipments


@app.post("/shipment")
def submit_shipment(shipment: Shipment) -> dict[str, Any]:
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "weight": shipment.weight,
        "content": shipment.content,
        "status": shipment.status
    }

    return {
        "message": f"Shipment with ID {new_id} added successfully.",
        "shipment_id": new_id
    }

'''
========
Enum
======== '''


# What is Enum?
# Enum (Enumeration) is used to define a fixed set of allowed values for a variable.
# It ensures that only predefined, meaningful values are accepted in the application.
# In your code, ShipmentStatus defines valid shipment states.
# refer schemas.py
class ShipmentStatus(Enum):
    placed = "Placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered= "delivered" 

@app.post("/shipment_update")
def update_data(id: int,body: dict[str, ShipmentStatus]) -> dict[str, Any]:
    shipments[id].update(body)
    return {"message": f'{id} updated successfully'}
    