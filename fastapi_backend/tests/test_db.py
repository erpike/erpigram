from src.models import User


def test_db_connection():
    assert User.select().count() == 0
