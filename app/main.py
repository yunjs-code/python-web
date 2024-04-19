from fastapi import FastAPI

app = FastAPI()

@app.get("/fetch-power-usage")
async def fetch_power_usage():
    url = "https://bigdata.kepco.co.kr/openapi/v1/powerUsage/industryType.do"
    # API 키와 필요한 파라미터 설정
    params = {
        "access_key": "38M6ESlslJK96g1366SPy0h11fsRr6os9cz2bRFF",  # 여기에 실제 액세스 키를 입력하세요.
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        return response.json()
