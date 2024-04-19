from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/get-power-usage/{year}/{month}/{metroCd}/{cityCd}")
def get_power_usage(year: int, month: int, metroCd: str, cityCd: str):
    url = "https://bigdata.kepco.co.kr/openapi/v1/powerUsage/industryType.do"
    params = {
        "apiKey": "38M6ESlslJK96g1366SPy0h11fsRr6os9cz2bRFF",  # 이 키는 예시일 뿐, 실제 운영에는 환경변수 사용을 권장
        "year": year,
        "month": month,
        "metroCd": metroCd,
        "cityCd": cityCd,
        "returnType": "json"
    }
    response = requests.get(url, params=params)
    return response.json()
