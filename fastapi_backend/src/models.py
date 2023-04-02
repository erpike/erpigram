from datetime import datetime

from peewee import Proxy, Model, CharField, DateTimeField, ForeignKeyField
from peewee_migrate import Router
from playhouse.sqlite_ext import SqliteExtDatabase

from config import DB_PATH, MIGRATIONS_PATH


db = SqliteExtDatabase(
    DB_PATH,
    autoconnect=False,
    pragmas={
        "foreign_keys": 1,
        "journal_mode": "wal",
    }
)
db_proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


class User(BaseModel):
    username = CharField(max_length=255)
    email = CharField(max_length=255)
    password = CharField(max_length=255)


class Post(BaseModel):
    image_url = CharField()
    image_url_type = CharField(max_length=255)
    caption = CharField(max_length=255)
    timestamp = DateTimeField(default=datetime.utcnow)
    user = ForeignKeyField(User, backref="posts")


def init_db():
    db_proxy.initialize(db)
    router = Router(db, migrate_dir=MIGRATIONS_PATH)
    with db_proxy:
        router.run()
        # TODO: create initial superuser
