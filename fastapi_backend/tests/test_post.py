import json

from src.models import User, Post


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


def test_get_post_list(fake_app):
    u1 = User.create(username="username", email="email", password="password")
    Post.create(image_url="/static/001.png", image_url_type="relative", caption="Hi there!", user=u1)
    Post.create(image_url="/static/002.png", image_url_type="relative", caption="My test...", user=u1)

    result = fake_app.get("/post")
    data = json.loads(result.text)
    for i in data:
        i.pop("timestamp")

    assert result.status_code == 200
    assert Post.select().count() == 2
    assert data == [
        {
            "id": 1,
            "caption": "Hi there!",
            "image_url": "/static/001.png",
            "image_url_type": "relative",
            "user": {"username": "username"},
        },
        {
            "id": 2,
            "caption": "My test...",
            "image_url": "/static/002.png",
            "image_url_type": "relative",
            "user": {"username": "username"},
        },
    ]
