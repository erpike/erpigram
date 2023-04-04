import json

from src.models import User, Post


def test_create_user_endpoint(fake_app):
    data = {"username": "username", "email": "email", "password": "password"}
    result = fake_app.post("/user", data=json.dumps(data))
    assert result.status_code == 200
    assert json.loads(result.text) == {k: v for k, v in data.items() if k != "password"}
    assert User.select().count() == 1


def test_create_post_endpoint(fake_app_authorized):
    user = User.create(username="admin", email="user@email", password="pwd")
    data = dict(
        image_url="https://img/url/absolute.png",
        image_url_type="absolute",
        caption="ico",
        user_id=user.id,
    )
    result = fake_app_authorized.post("/post", data=json.dumps(data))
    assert result.status_code == 200
    assert Post.select().count() == 1
    assert {k: v for k, v in json.loads(result.text).items() if k != "timestamp"} == {
        "id": 1,
        "caption": "ico",
        "image_url": "https://img/url/absolute.png",
        "image_url_type": "absolute",
        "user": {"username": "admin"},
    }
