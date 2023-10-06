import os.path

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from config import IMAGE_PATH, STATIC_PATH
from src.models import init_db
from src.routes.auth import router as auth_router
from src.routes.post import router as post_router
from src.routes.user import router as user_router
from src.routes.comment import router as comment_router


origins = [
    "http://localhost:3000",  # react js app runs on port 3000 by default
    # "http://localhost:8000",
]


class ErpigramFastAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init()

    @staticmethod
    def create_static_folders():
        for path in (STATIC_PATH, IMAGE_PATH):
            if not os.path.exists(path):
                os.makedirs(path)

    @staticmethod
    def init_database():
        init_db()

    def init(self):
        self.init_database()
        self.create_static_folders()
        self.include_router(auth_router)
        self.include_router(comment_router)
        self.include_router(post_router)
        self.include_router(user_router)

        self.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,  # allow login/logout (auth headers)
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.mount("/images", StaticFiles(directory=IMAGE_PATH), name="images")
