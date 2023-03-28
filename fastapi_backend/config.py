import os

SRC_DIR = os.path.dirname(__file__)

DB_PATH = os.path.join(SRC_DIR, "ergram.sqlite")
MIGRATIONS_PATH = os.path.join(SRC_DIR, "db", "migrations")
