import logging

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles, FileResponse
from uvicorn import run

from mce.v1_api import app as v1_api_app

logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.mount("/v1", v1_api_app)
app.mount("/static", StaticFiles(directory="pages/static"), name="static")


@app.get("/")
async def homepage():
    """
    To document
    """
    return FileResponse("pages/home.html")


@app.get("/health")
async def health():
    """
    Health check interface
    """
    return {"status": "success"}


# This is for debugging, use uvicorn api_service:app --host 0.0.0.0 --port 8000.... for deployment
if __name__ == '__main__':
    run(app, host="127.0.0.1", port=8000)
