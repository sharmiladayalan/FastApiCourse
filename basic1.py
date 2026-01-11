from fastapi import FastAPI
from typing import Any

app = FastAPI()

@app.get("/shipment")
def get_shipment():
    return {
        "content" : "Wooden table",
        "status"  : "In transit"
              }

# path parameter
@app.get("/shipment/{id}")
def get_shipment_id(id: int) -> dict[str,Any]:
    return {
        "id" : id,
        "content" : "Wooden table",
        "status"  : "In transit"
            }
