from fastapi import FastAPI, status, HTTPException
from typing import Any,Optional

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

'''
=============
HTTP Exception
==============
'''
#Getting an error with status query parameter in http request
@app.get("/shipment_http")
def get_shipments(id: int):
    if id not in shipments:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "requested id doesn't exist"
        )
    return shipments[id]


'''
===============
Put Method
===============
'''

#getting an user Id from user and updating the shipment status
@app.put("/shipment")
def add_data(id: int, weight: float, content: str, shipment_status: str):
    if id in shipments:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Shipment ID already exists"
        )
    else:
        shipments[id] ={
            "weight" : weight,
            "content" : content,
            "status" : shipment_status }
        return {"message": f"shipment {shipments[id]} added successfully"}
    
#Now auto increment the shipment ID by using previous id (usinf max function)
@app.put("/shipment_auto")
def add_data_auto(content: str, weight: float, shipment_status: str):
    #Validate Weight
    if weight >= 25:
        raise(HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail= "Weight should not be more than 25Kg"
        ))
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "weight": weight,
        "content": content,
        "status": shipment_status
    }
    return {"message": f"Shipment with ID {new_id} added successfully."}

@app.put("/shipment_update/{id}")
def update_shipment(id: int, weight: float, content: str, shipment_status: str):
    shipments[id] = {
        "weight": weight,
        "content": content,
        "status": shipment_status
    }
    return shipments[id]

#By using this post we can update insert or update entire date but we cannot update single field 
#For this we use patch method
'''
=============
Patch Method
=============
 '''
@app.patch("/shipment_update/{id}")
def patch_shipment(
    id: int,
    content: Optional[str] = None,
    weight: Optional[float] = None,
    status: Optional[str] = None
):
    if id not in shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    shipment = shipments[id]
    #Now shipment local variable contains the data of shipments[id] 
    #For example 1223:{"weight" : 5.8,"content" : "Wooden table","status"  : "In transit"}

    if content is not None:
        shipment["content"] = content
    if weight is not None:
        shipment["weight"] = weight
    if status is not None:
        shipment["status"] = status

    shipments[id] = shipment
    #Now we update the data in shipment local variable to shipments dictionary
    return shipment

@app.patch("/shipment")
def patch_shipment_1(id: int, body: dict[str, Any]):
    shipment = shipments[id]
    shipment.update(body)
    shipments[id] = shipment
    return shipment

'''
============
Delete
============
'''
@app.delete("/shipment/{id}")
def delete_shipment(id: int) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(status_code=404, detail="Shipment ID not Found")
    del shipments[id]
    # shipments.pop(id)
    return {"Message": f'Shipment ID {id} deleted successfully'}

