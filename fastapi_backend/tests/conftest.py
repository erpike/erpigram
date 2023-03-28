import pytest

from playhouse.sqlite_ext import SqliteExtDatabase

from src.models import db_proxy, BaseModel


db = SqliteExtDatabase(":memory:")


@pytest.fixture(scope="function", autouse=True)
def init_test_db():
    with db_proxy:
        models = [cls for cls in BaseModel.__subclasses__()]
        db_proxy.drop_tables(models)
        db_proxy.create_tables(models)


@pytest.fixture(scope="session", autouse=True)
def initialize_db():
    db_proxy.initialize(db)
    with db_proxy:
        yield
