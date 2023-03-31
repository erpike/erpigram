import os
import pytest

from playhouse.sqlite_ext import SqliteExtDatabase
from starlette.testclient import TestClient

from main import app
from src.models import db_proxy, BaseModel

test_db = "testdb.sqlite"
db = SqliteExtDatabase(
    test_db,
    autoconnect=False,
    pragmas={"foreign_keys": 1},
)


@pytest.fixture()
def fake_app():
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def init_test_db():
    with db_proxy:
        models = [cls for cls in BaseModel.__subclasses__()]
        db_proxy.drop_tables(models)
        db_proxy.create_tables(models)

        # For some strange reason TestClient().post could not write to db as db locked
        # committing session releases db resources (maybe)
        db_proxy.commit()

        yield


@pytest.fixture(scope="session", autouse=True)
def initialize_db():
    db_proxy.initialize(db)
    yield
    os.remove(test_db) if os.path.exists(test_db) else None
