from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.notion import add_to_notion_database

app = FastAPI()

# Static 파일 제공 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_form():
    html_content = """
    <html>
        <head>
            <title>Submit to Notion</title>
        </head>
        <body>
            <h1>Submit a Title to Notion</h1>
            <form action="/submit" method="post">
                <label for="title">Title:</label>
                <input type="text" id="title" name="title">
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/submit")
async def submit_form(title: str = Form(...)):
    data = {"title": title}
    status_code, response_json = add_to_notion_database(data)
    return {"status_code": status_code, "response": response_json}
