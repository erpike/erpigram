from src.models import User, Post


def test_db_connection():
    assert User.select().count() == 0


def test_post_on_delete_user():
    user = User.create(username="admin", email="email", password="pass")
    user2 = User.create(username="rsc", email="rsc", password="pass")
    Post.create(image_url="url", image_url_type="absolute", caption="Test", user=user)
    Post.create(image_url="url2", image_url_type="absolute", caption="Test2", user=user)
    Post.create(image_url="url3", image_url_type="absolute", caption="Test3", user=user2)
    user.delete_instance()
    assert list(User.select(User.id, User.username).tuples()) == [(2, "rsc")]
    assert list(Post.select(Post.id, Post.caption, Post.user).tuples()) == [
        (1, "Test", None),
        (2, "Test2", None),
        (3, "Test3", 2),
    ]
