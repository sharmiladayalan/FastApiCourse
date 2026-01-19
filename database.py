import sqlite3
from typing import Any
from schemas import ShipmentCreate, ShipmentUpdate

class Database:
    def __init__(self):
        # Make the connection
        self.conn = sqlite3.connect("sqlite.db")
        # Get cursor to execute queries and fetch data
        self.cur = self.conn.cursor()
        self.create_table("shipment")

    def create_table(self, name: str):
        # 1.Create a table
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS ?(
                         id INTEGER PRIMARY KEY,
                         content TEXT, 
                         weight REAL,
                          status TEXT)""", (name,))
        
    def create(self, shipment: ShipmentCreate):
        self.cur.execute("SELECT MAX(id) FROM shipment")
        result = self.cur.fetchone()
        new_id = result[0] +1

        # 2. Insert records
        self.cur.execute("""INSERT INTO shipment
                        VALUES (:id, :content, :weight, :status)""",
                         {
                             "id": new_id,
                             **shipment.model_dump(),
                             "status": "placed",
                         })
        self.conn.commit()

        def get(self, id: int) -> dict[str, Any]:
            # 3. Read the data
            self.cur.execute("SELECT * FROM shipment WHERE id = ?", (id,))
            row = self.cur.fetchone()

            if row is None:
                return {"status": "Not Found"}
            
            return {
                "id": row[0],
                "content": row[1],
                "weight": row[2],
                "status": row[3],
            }

        def update(self, shipment: ShipmentUpdate) -> dict[str, Any]:
            self.cur.execute(""" UPDATE shipment SET status = :status 
                             WHERE id = :id""",
                             {
                                 "id": shipment.id,
                                **shipment.model_dump()
                             })
            self.conn.commit()
            return self.get(shipment.id)
            
        def delete(self, id: int):
            self.cur.executr(""" DELETE FROM shipment 
                             WHERE id = :id""",
                             {
                                 id: id
                             })
            self.conn.commit()

        def close():
            self.conn.close()