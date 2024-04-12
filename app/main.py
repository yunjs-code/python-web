from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 데이터 모델 정의
class Item(BaseModel):
    name: str

# 메모리 내 데이터 저장소
items = {}

# POST 요청으로 데이터를 받아 저장하는 엔드포인트
@app.post("/items/")
def create_item(item: Item):
    if item.name in items:
        return {"Error": "Item with this name already exists"}
    items[item.name] = item
    return item

# GET 요청으로 데이터를 조회하는 엔드포인트
@app.get("/items/{item_name}")
def read_item(item_name: str):
    return items.get(item_name, {"Error": "Item not found"})
