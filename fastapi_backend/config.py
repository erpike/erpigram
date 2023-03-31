import os

ROOT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(ROOT_DIR, "src")

MIGRATIONS_PATH = os.path.join(SRC_DIR, "db", "migrations")
DB_PATH = os.path.join(ROOT_DIR, "ergram.sqlite")
