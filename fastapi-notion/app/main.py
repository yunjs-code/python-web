import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

# 환경 변수 로드
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_URL = "https://testapi.openbanking.or.kr/oauth/2.0/authorize"
TOKEN_URL = "https://testapi.openbanking.or.kr/oauth/2.0/token"
FRONTEND_URI = os.getenv("FRONTEND_URI")
STATE = "12345678901234567890123456789012"
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInfo(BaseModel):
    name: str
    email: str
    password: str
    access_token: str
    refresh_token: str
    user_seq_no: str

@app.get("/login")
def login():
    redirect_uri = f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=login inquiry transfer&state={STATE}&auth_type=0"
    logging.debug(f"Authorization URL: {redirect_uri}")
    return RedirectResponse(redirect_uri)

@app.get("/callback")
def callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    if not code or state != STATE:
        return JSONResponse(status_code=400, content={"error": "Invalid state or no code provided"})

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(TOKEN_URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"})
    if response.status_code != 200:
        return JSONResponse(status_code=400, content={"error": "Failed to obtain access token"})

    token_data = response.json()
    redirect_url = f"{FRONTEND_URI}?access_token={token_data['access_token']}&refresh_token={token_data.get('refresh_token', '')}&user_seq_no={token_data['user_seq_no']}"
    return RedirectResponse(redirect_url)

@app.post("/save_user_info")
def save_user_info(user_info: UserInfo):
    required_keys = ["name", "email", "password", "access_token", "refresh_token", "user_seq_no"]
    missing_keys = [key for key in required_keys if not getattr(user_info, key)]
    if missing_keys:
        logging.error(f"Missing keys: {', '.join(missing_keys)}")
        return JSONResponse(status_code=400, content={"error": f"Missing keys in request: {', '.join(missing_keys)}"})

    notion_url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-08-16"
    }

    request_data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "name": {"title": [{"text": {"content": user_info.name}}]},
            "email": {"email": user_info.email},
            "password": {"rich_text": [{"text": {"content": user_info.password}}]},
            "access_token": {"rich_text": [{"text": {"content": user_info.access_token}}]},
            "refresh_token": {"rich_text": [{"text": {"content": user_info.refresh_token}}]},
            "user_seq_no": {"rich_text": [{"text": {"content": user_info.user_seq_no}}]}
        }
    }
    logging.debug(f"Notion API request data: {request_data}")

    response = requests.post(notion_url, headers=headers, json=request_data)

    logging.debug(f"Notion API response status: {response.status_code}")
    logging.debug(f"Notion API response content: {response.text}")

    if response.status_code != 200:
        logging.error(f"Failed to save user info to Notion: {response.text}")
        return JSONResponse(status_code=400, content={"error": "Failed to save user info to Notion"})

    return JSONResponse(status_code=200, content={"message": "User info saved successfully"})
