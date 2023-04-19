from src.models import User, Post, Comment, db_proxy, get_db_models_list
from src.utils import PwdManager


def clean_db():
    with db_proxy:
        for model in get_db_models_list():
            model.delete().execute()


def populate_db_by_dummy_data():
    with db_proxy:
        admin_user = User.create(username="admin", password=PwdManager.hash(" "), email="admin@no.mail")
        rsc_user = User.create(username="rsc", password=PwdManager.hash(" "), email="rsc@no.mail")

        post1 = Post.create(
            image_url="https://cdn.pixabay.com/photo/2017/08/30/01/05/milky-way-2695569__480.jpg",
            image_url_type="absolute",
            caption="Space is awesome",
            user=admin_user,
        )

        post2 = Post.create(
            image_url="https://i2.cdn.turner.com/cnnnext/dam/assets/221216133203-best-space-photos-2022-card.jpg",
            image_url_type="absolute",
            caption="Galaxy vortex",
            user=rsc_user,
        )

        Comment.create(post=post1, text="Beautiful stars...", user=admin_user)
        Comment.create(post=post2, text="Like mana whatever", user=admin_user)
        Comment.create(post=post2, text="Wat?", user=rsc_user)


def refresh_db_data():
    clean_db()
    populate_db_by_dummy_data()
