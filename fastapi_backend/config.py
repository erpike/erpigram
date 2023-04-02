import os

ROOT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(ROOT_DIR, "src")

MIGRATIONS_PATH = os.path.join(SRC_DIR, "db", "migrations")
DB_PATH = os.path.join(ROOT_DIR, "ergram.sqlite")

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 mins
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt_secret")  # openssl rand -hex 32
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY", "jwt_refresh_secret")
