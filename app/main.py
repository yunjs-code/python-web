from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/get-power-usage/{year}/{month}/{metroCd}/{cityCd}")
def get_power_usage(year: int, month: int, metroCd: str, cityCd: str):
    url = "https://bigdata.kepco.co.kr/openapi/v1/powerUsage/industryType.do"
    params = {
        "apiKey": "38M6ESlslJK96g1366SPy0h11fsRr6os9cz2bRFF",  # 환경 변수에서 가져오는 것을 추천
        "year": year,
        "month": month,
        "metroCd": metroCd,
        "cityCd": cityCd,
        "returnType": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {"error": "API 요청 실패", "statusCode": response.status_code, "details": response.text}
    return response.json()
