from fastapi import FastAPI

from src.models import init_db

app = FastAPI(title="ErpiGRAM")
init_db()


@app.get("/")
def root():
    return "Hello world"
