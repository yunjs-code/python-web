from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
import requests
from app.models import UserInfo, LoginInfo
from app.config import NOTION_API_KEY, NOTION_DATABASE_ID
from app.utils import post_to_notion

router = APIRouter()

@router.post("/save_user_info")
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

    response = post_to_notion(notion_url, headers, request_data)

    if response.status_code != 200:
        logging.error(f"Failed to save user info to Notion: {response.text}")
        return JSONResponse(status_code=400, content={"error": "Failed to save user info to Notion"})

    return JSONResponse(status_code=200, content={"message": "User info saved successfully"})

@router.post("/login_user")
def login_user(login_info: LoginInfo):
    notion_url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-08-16"
    }

    response = requests.post(notion_url, headers=headers, json={"filter": {"property": "name", "rich_text": {"equals": login_info.name}}})
    if response.status_code != 200:
        logging.error(f"Failed to query user info from Notion: {response.text}")
        return JSONResponse(status_code=400, content={"error": "Failed to query user info from Notion"})

    results = response.json().get("results")
    if not results:
        return JSONResponse(status_code=400, content={"error": "User not found"})

    stored_password = results[0]["properties"]["password"]["rich_text"][0]["text"]["content"]
    if stored_password != login_info.password:
        return JSONResponse(status_code=400, content={"error": "Invalid password"})

    return JSONResponse(status_code=200, content={"message": "Login successful"})
