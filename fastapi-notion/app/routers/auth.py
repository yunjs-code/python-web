from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
import requests
import logging
from app.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, STATE, TOKEN_URL, FRONTEND_URI

router = APIRouter()

@router.get("/login")
def login():
    redirect_uri = f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=login inquiry transfer&state={STATE}&auth_type=0"
    logging.debug(f"Authorization URL: {redirect_uri}")
    return RedirectResponse(redirect_uri)

@router.get("/callback")
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
