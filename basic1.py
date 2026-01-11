from fastapi import FastAPI
from typing import Any

app = FastAPI()


#sample bulk data for shipment 
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

''' 
==============
Path parameter
==============
'''

#To get all shipments
@app.get("/shipments")
def get_all_shipment():
    return shipments

# we nee to get an latest updated shipment so, which shipment id is greater is added at last
# For that we find an max key value
@app.get("/shipment/latest")
def get_shipment_latest() -> dict[str,Any]:
    id = max(shipments.keys())
    return shipments[id]

# path parameter
#if we give an id then it will take as input
@app.get("/shipment/{id}")
def get_shipment_id(id: int) -> dict[str,Any]:
    return {
        "id" : id,
        "content" : "Wooden table",
        "status"  : "In transit"
            }

@app.get("/shipments/{id}") 
def get_shipments_id(id: int):
    if id in shipments:
        return shipments[id]
    return {"message": "Shipment ID not found"}


# @app.get("/scalar", include_in_schema=False)
# def get_scalar_docs():

''' 
=============
Query Parameter
=============

To declare query parameter we need to add ? after the path parameter
'''
@app.get("/shipment_query")
def get_shipment_by_status(status):
    result = []
    for shipment_id in shipments:
        if shipments[shipment_id]["status"] == status:
            result.append({shipment_id: shipments[shipment_id]})
        return result
    return {"message": "No shipments with the given status"}

'''
=================================
Path and query parameter together
=================================
'''
#In this if we give an field name as path parameter and id as query parameter
#http://127.0.0.1:8000/shipment_details/content?id=1227


@app.get("/shipment_details/{field}")
def get_shipment_by_condition(field: str,id: int) -> dict[str,Any]:
    return {
        field: shipments[id][field]
    }

