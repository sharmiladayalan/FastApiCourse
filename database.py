# import json

# shipments = {}

# with open("shipment.json") as json_file:
#     data = json.load(json_file)
#     for value in data:
#         shipments[value["id"]] = value
# # print(shipments)

# def save():
#     with open("shipment.json", "w") as json_file:
#         json.dump(list(shipments.values()), json_file, indimport sq
    
import sqlite3
# Mke the connection
connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

# 1.Create a table
cursor.execute("CREATE TABLE IF NOT EXISTS shipment(id INTEGER PRIMARY KEY, content TEXT, weight REAL, status TEXT)")

# Insert records
# cursor.execute("INSERT INTO shipment VALUES(2, 'Bag', 0.5, 'Placed')")
# connection.commit()

# Read the data
# Using fetch all
# cursor.execute("SELECT * FROM shipment ")
# result = cursor.fetchall()
# print(result)

# Using fetchmany
# cursor.execute("SELECT * FROM shipment ")
# result = cursor.fetchmany(2)
# print(result)

# # Using fetchone
# cursor.execute("SELECT * FROM shipment ")
# result = cursor.fetchone()
# print(result)

# Delete a shipment by id
# cursor.execute("DELETE FROM shipment WHERE id = 2")
# connection.commit()

# Drop table
# cursor.execute("DROP TABLE shipment")
# connection.commit()

# Update The shipment data
# cursor.execute("UPDATE shipment SET status ='In transit' WHERE id = 1")
# connection.commit()

# Update the value using formated  string
id=2
status ="Out for delivery"
cursor.execute(
    f'UPDATE shipment SET status = "{status}" WHERE id = {id}'
)
connection.commit()

# Using placeholders to avoid SQL injection
id = 1
status ="Delivered"
cursor.execute("UPDATE shipment SET status =  ? WHERE id = ?", (status,id))
connection.commit()

# Using named placeholders
id = 1
status ="Delivered"
cursor.execute("UPDATE shipment SET status = :status WHERE id = :id", {"status": status, "id": id})
connection.commit()











# Close the connection  when done
connection.close
