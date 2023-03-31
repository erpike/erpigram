import json

from src.models import User


def test_create_user_endpoint(fake_app):
    data = {"username": "username", "email": "email", "password": "password"}
    result = fake_app.post("/user", data=json.dumps(data))
    assert result.status_code == 200
    assert json.loads(result.text) == {k: v for k, v in data.items() if k != "password"}
    assert User.select().count() == 1
