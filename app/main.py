from fastapi import FastAPI

app = FastAPI()

items = {}

@app.post("/items/{item_name}")
def create_item(item_name: str):
    if item_name in items:
        return {"Error": "Item already exists"}
    items[item_name] = item_name
    return {"item_name": item_name}

@app.get("/items/{item_name}")
def read_item(item_name: str):
    return {"item_name": items.get(item_name, "Not found")}

@app.put("/items/{item_name}")
def update_item(old_name: str, new_name: str):
    if old_name not in items:
        return {"Error": "Item not found"}
    items[new_name] = items.pop(old_name)
    return {"item_name": new_name}

@app.delete("/items/{item_name}")
def delete_item(item_name: str):
    if item_name not in items:
        return {"Error": "Item not found"}
    del items[item_name]
    return {"message": "Item deleted successfully"}
