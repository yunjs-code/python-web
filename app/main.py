from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/get-power-usage")
def get_power_usage():
    url = "https://bigdata.kepco.co.kr/openapi/v1/powerUsage/industryType.do"
    params = {
        "api_key": "38M6ESlslJK96g1366SPy0h11fsRr6os9cz2bRFF",
    }
    response = requests.get(url, params=params)
    return response.json()
