import os
import pytest
from _pytest.fixtures import SubRequest

from playhouse.sqlite_ext import SqliteExtDatabase
from starlette.testclient import TestClient

from main import app
from src.models import db_proxy, get_db_models_list
from src.routes.auth import identify_user


test_db = "testdb.sqlite"
db = SqliteExtDatabase(
    test_db,
    autoconnect=False,
    pragmas={"foreign_keys": 1},
)


@pytest.fixture
def fake_app():
    return TestClient(app)


@pytest.fixture
def fake_app_authorized():
    def fake_auth():
        return "auth_user"
    app.dependency_overrides[identify_user] = fake_auth
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def init_test_db(request: SubRequest):
    if "nodb" in request.keywords:
        yield
        return

    with db_proxy:
        models = get_db_models_list()
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
