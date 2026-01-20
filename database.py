import sqlite3
from typing import Any
from schemas import ShipmentCreate, ShipmentUpdate

class Database:
    def connect_to_db(self):
        # Make the connection
        self.conn = sqlite3.connect("sqlite.db")
        print("Database connected successfully")
        # Get cursor to execute queries and fetch data
        self.cur = self.conn.cursor()

    def create_table(self, name: str):
        # 1.Create a table
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {name} (
            id INTEGER PRIMARY KEY,
            content TEXT,
            weight REAL,
            status TEXT
        )
    """)
        self.conn.commit()

        
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
        self.cur.execute(""" DELETE FROM shipment 
                             WHERE id = :id""",
                             {
                                 id: id
                             })
        self.conn.commit()

    def close(self):
        self.conn.close()

    def __enter__(self):
        print("Entered into context")
        self.connect_to_db()
        self.create_table('shipment')
        return self

    def __exit__(self,*args):
        print("Exiting from context")
        self.close()

# This is an actual steps to use database 
# We need to create an object first and then use it then we need to close it every time 
''' db = Database()

db.get(1225)

db.close() '''

# To manage this use context manager with 'with' statement

# For example
# with open('file.txt') as file:
#     file.read()

with Database() as db:
    print(db.get(1))
'''
How the context manager works:
1) When the execution reaches the 'with' statement , it calls the __enter__ method of the Database class
2) The __enter__ method establishes the database connection and creates the table if it doesn't exist
3) The database object is returned and assigned to the variable db
4) Inside the 'with' block, you can use the db object to perform database operations
5) When the execution leaves the 'with' block, the __exit__ method of the Database class is automatically called
6) The __exit__ method closes the database connection, ensuring that resources are properly released
'''
