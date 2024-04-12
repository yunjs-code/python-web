from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str

items = {}

@app.post("/items/")
def create_item(item: Item):
    if item.name in items:
        return {"Error": "Item already exists."}
    items[item.name] = item
    return item

@app.get("/items/{item_name}")
def read_item(item_name: str):
    if item_name in items:
        return items[item_name]
    return {"Error": "Item not found."}

@app.get("/echo/")
def echo_name(name: str = Query(None, description="Enter your name to echo")):
    return {"Echoed Name": name}
