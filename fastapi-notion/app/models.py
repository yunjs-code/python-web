from pydantic import BaseModel

class UserInfo(BaseModel):
    name: str
    email: str
    password: str
    access_token: str
    refresh_token: str
    user_seq_no: str

class LoginInfo(BaseModel):
    name: str
    password: str
