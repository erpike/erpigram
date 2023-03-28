from src.models import User


def test_db_connection():
    User.create(username="username", email="email", password="pass")
    assert User.select().count() == 1
