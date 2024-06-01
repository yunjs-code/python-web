import logging
from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_URL = "https://testapi.openbanking.or.kr/oauth/2.0/authorize"
TOKEN_URL = "https://testapi.openbanking.or.kr/oauth/2.0/token"
FRONTEND_URI = "http://localhost:3000"
STATE = "12345678901234567890123456789012"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/login")
def login():
    logging.debug("Redirecting to authorization URL.")
    redirect_uri = (
        f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&scope=login inquiry transfer&"
        f"state={STATE}&auth_type=0"
    )
    logging.debug(f"Authorization URL: {redirect_uri}")
    return RedirectResponse(redirect_uri)

@app.get("/callback")
def callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    logging.debug(f"Received code: {code}, state: {state}")
    if not code or state != STATE:
        logging.error("Invalid state or no code provided")
        return {"error": "Invalid state or no code provided"}

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    logging.debug(f"Requesting token with data: {data}")
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    if response.status_code != 200:
        logging.error(f"Failed to obtain access token: {response.text}")
        return {"error": "Failed to obtain access token"}

    token_data = response.json()
    logging.debug(f"Received token data: {token_data}")
    access_token = token_data["access_token"]
    refresh_token = token_data.get("refresh_token", "")
    user_seq_no = token_data["user_seq_no"]

    redirect_url = (
        f"{FRONTEND_URI}?access_token={access_token}"
        f"&refresh_token={refresh_token}&user_seq_no={user_seq_no}"
    )
    logging.debug(f"Redirecting to frontend with URL: {redirect_url}")
    return RedirectResponse(redirect_url)

@app.post("/save_user_info")
def save_user_info(user_info: dict):
    logging.debug(f"Saving user info: {user_info}")
    notion_url = "https://api.notion.com/v1/pages"
    notion_token = os.getenv("NOTION_TOKEN")
    notion_db_id = os.getenv("NOTION_DB_ID")

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-08-16"
    }

    data = {
        "parent": {"database_id": notion_db_id},
        "properties": {
            "Name": {"title": [{"text": {"content": user_info["name"]}}]},
            "Email": {"email": user_info["email"]},
            "Password": {"rich_text": [{"text": {"content": user_info["password"]}}]},
            "Access Token": {"rich_text": [{"text": {"content": user_info["access_token"]}}]},
            "Refresh Token": {"rich_text": [{"text": {"content": user_info["refresh_token"]}}]},
            "User Seq No": {"rich_text": [{"text": {"content": user_info["user_seq_no"]}}]}
        }
    }

    logging.debug(f"Sending data to Notion: {data}")
    response = requests.post(notion_url, headers=headers, json=data)
    if response.status_code != 200:
        logging.error(f"Failed to save user info to Notion: {response.text}")
        return {"error": "Failed to save user info"}
    
    logging.debug("User info saved successfully")
    return {"message": "User info saved successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
