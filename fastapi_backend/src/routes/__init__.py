from src.models import db_proxy


def db_session():
    with db_proxy:
        yield
