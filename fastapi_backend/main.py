from fastapi import FastAPI

from src.models import init_db
from src.routes.user import router


app = FastAPI(title="ErpiGRAM")
app.include_router(router)


init_db()


@app.get("/")
def root():
    return "Hello world"
