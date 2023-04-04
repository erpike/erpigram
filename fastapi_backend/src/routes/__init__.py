from src.models import db_proxy


async def db_session():
    with db_proxy as session:
        yield session

