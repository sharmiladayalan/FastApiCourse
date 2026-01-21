# from contextlib import asynccontextmanager
# from rich.console import Console
# from rich.panel import Panel
# from fastapi import FastAPI

# @asynccontextmanager
# async def lifespan_handler(app: FastAPI):
#     Console.print(Panel("Server started....", border_style="green"))
#     yield
#     Console.print(Panel("......stopped", border_style="red"))
   

# app = FastAPI(lifespan=lifespan_handler)
# @app.get("/")
# def read_root():
#     return {"detail":"server is running"}

from contextlib import asynccontextmanager
from rich.console import Console
from rich.panel import Panel
from fastapi import FastAPI

console = Console()   # 👈 instance

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    console.print(Panel("Server started....", border_style="green"))
    yield
    console.print(Panel("......stopped", border_style="red"))

app = FastAPI(lifespan=lifespan_handler)

@app.get("/")
def read_root():
    return {"detail": "server is running"}
