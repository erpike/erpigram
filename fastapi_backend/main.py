from fastapi import FastAPI

from src.models import init_db
from src.routes.post import router as post_router
from src.routes.user import router as user_router


app = FastAPI(title="ErpiGRAM")
app.include_router(post_router)
app.include_router(user_router)
init_db()
