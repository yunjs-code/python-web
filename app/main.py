from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

user_name = "이동하"

class User(BaseModel):
    name: str


user1=User(name="dongha hihi")


@app.post("/user/")
async def receive_user(user: User):
    global user_name
    user_name = user.name
    return {"message": "User name received"}


@app.get("/user/")
async def get_user():
    return {"user_name": user_name}

@app.put("/user/")
async def receive_user(user: User):
    global user_name
    user_name = user.name
    return {"message": "User name changed"}


@app.delete("/user/")
async def del_user():
    global user_name
    user_name = "DELETED"
    return {"message": "User name deleted"}
