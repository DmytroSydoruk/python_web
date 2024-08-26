from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.modules.mvc.router import router as mvc_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(mvc_router)
