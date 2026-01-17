import json

shipments = {}

with open("shipment.json") as json_file:
    data = json.load(json_file)
    for value in data:
        shipments[value["id"]] = value
# print(shipments)

def save():
    with open("shipment.json", "w") as json_file:
        json.dump(list(shipments.values()), json_file, indent=4)


    

