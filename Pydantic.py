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
from fastapi import FastAPI, HTTPException, status
# from schemas import Shipment
from typing import Any
from schemas import BaseShipment, ShipmentRead, ShipmentCreate, ShipmentStatus, ShipmentUpdate
from database import shipments,save
app = FastAPI()
# shipments ={
#     1223:{
#     "weight" : 5.8,
#     "content" : "Wooden table",
#     "status"  : "In transit"
#     },
#     1224:{
#     "weight" : 3.2,
#     "content" : "Metal chair",
#     "status"  : "Delivered"
#     },
#     1225:{
#     "weight" : 12.5,
#     "content" : "Glass bookshelf",
#     "status"  : "In transit"
#     },
#     1226:{
#     "weight" : 8.7,
#     "content" : "Wooden desk",
#     "status"  : "Pending"
#     },
#     1227:{
#     "weight" : 2.1,
#     "content" : "Lamp",
#     "status"  : "Delivered"
#     },
#     1228:{
#     "weight" : 6.4,
#     "content" : "Sofa",
#     "status"  : "In transit"
#     }
# }

@app.get("/shipments")
def get_all_shipment():
    return shipments


# @app.post("/shipment", response_model="None")
# def submit_shipment(shipment: Shipment) -> dict[str, Any]:
#     new_id = max(shipments.keys()) + 1

#     shipments[new_id] = {
#         "weight": shipment.weight,
#         "content": shipment.content,
#         "status": shipment.status
#     }

#     return {
#         "message": f"Shipment with ID {new_id} added successfully.",
#         "shipment_id": new_id
#     }

'''
========
Enum
======== '''


# What is Enum?
# Enum (Enumeration) is used to define a fixed set of allowed values for a variable.
# It ensures that only predefined, meaningful values are accepted in the application.
# In your code, ShipmentStatus defines valid shipment states.
# refer schemas.py
'''class ShipmentStatus(Enum):
    placed = "Placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered= "delivered" 

@app.post("/shipment_update")
def update_data(id: int,body: dict[str, ShipmentStatus]) -> dict[str, Any]:
    shipments[id].update(body)
    return {"message": f'{id} updated successfully'} '''
    
'''
==================
Response Model
=================='''
# Why response_model
# response_model is used to control and validate what data the API sends back to the client.
# It filters extra fields
# It ensures correct data types
# It returns a fixed, clean response format

@app.get("/shipment_response/{id}", response_model=BaseShipment)
def get_shipment_response(id: int) :
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return  shipments[id]
    
'''
======================
Multiple response models
======================'''
# refer schemas.py
# Why Multiple Response Models are Used??
# APIs do not always return the same type of response.
# Depending on the action or result, the response structure changes.
# So, we use multiple response models to clearly define each possible response format.
@app.get("/shipment_mul_response/{id}", response_model=ShipmentRead)
def get_shipment_mul_response(id: int) :
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return shipments[id]


# @app.post("/shipment_update_response", response_model=ShipmentCreate)
# def update_data_response(id: int,body: dict[str, ShipmentStatus]) -> dict[str, Any]:
#     shipments[id].update(body)
#     return {"message": f'{id} updated successfully'}
# from fastapi import HTTPException

@app.patch("/shipment/{id}")
def update_shipment_status(id: int, body: ShipmentUpdate):
    if id not in shipments:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    shipments[id]["status"] = body.status.value
    save()

    return shipments[id]
