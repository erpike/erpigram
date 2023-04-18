import json

import pytest

from src.models import User, Post, Comment


def test_create_comment_endpoint(fake_app_authorized):
    User.create(username="admin", email="user@email", password="pwd")
    Post.create(
        image_url="url",
        image_url_type="type",
        caption="Title 1",
        user_id=1,
    )
    data = dict(
        post_id=1,
        text="my comment",
        user_id=1,
    )
    result = fake_app_authorized.post("/comment", data=json.dumps(data))
    assert result.status_code == 200
    assert Comment.select().count() == 1
    assert {k: v for k, v in json.loads(result.text).items() if k != "timestamp"} == {
        "text": "my comment", "user": {"username": "admin"}
    }


@pytest.mark.parametrize("post_id, user_id", [
    (1, 2), (2, 1)
])
def test_create_comment_endpoint_comment_not_found(fake_app_authorized, post_id, user_id):
    User.create(username="admin", email="user@email", password="pwd")
    Post.create(
        image_url="url",
        image_url_type="type",
        caption="Title 1",
        user_id=1,
    )
    data = dict(
        post_id=post_id,
        text="my comment",
        user_id=user_id,
    )

    result = fake_app_authorized.post("/comment", data=json.dumps(data))
    assert result.status_code == 404
    assert Comment.select().count() == 0
    assert result.text == '{"detail":"Either of parameter `post_id` / `user_id` is invalid (Does not exist)."}'


@pytest.mark.parametrize("post_id, out", [
    (1, [{"text": "text 1 (by username)", "user": {"username": "username"}}]),
    (
        2,
        [
            {"text": "text 2 (by username)", "user": {"username": "username"}},
            {"text": "text 1 (by admin)", "user": {"username": "admin"}},
        ]
    ),
])
def test_get_comments_list(fake_app, post_id, out):
    u1 = User.create(username="username", email="email", password="password")
    u2 = User.create(username="admin", email="ad@email", password="password")
    p1 = Post.create(image_url="/static/001.png", image_url_type="relative", caption="Hi there!", user=u1)
    p2 = Post.create(image_url="/static/002.png", image_url_type="relative", caption="My test...", user=u2)

    Comment.create(user=u1, post=p1, text="text 1 (by username)")
    Comment.create(user=u1, post=p2, text="text 2 (by username)")
    Comment.create(user=u2, post=p2, text="text 1 (by admin)")

    result = fake_app.get(f"/comment/all/{post_id}")
    data = json.loads(result.text)
    for i in data:
        i.pop("timestamp")

    assert result.status_code == 200
    assert data == out
