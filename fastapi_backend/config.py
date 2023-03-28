import os

ROOT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(ROOT_DIR, "src")
DB_PATH = os.path.join(SRC_DIR, "ergram.sqlite")
MIGRATIONS_PATH = os.path.join(SRC_DIR, "db", "migrations")
