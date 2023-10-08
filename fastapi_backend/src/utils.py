import argparse
import random
import string
from datetime import datetime, timedelta, timezone
from functools import partial
from typing import Union, Any

import jwt
from passlib.context import CryptContext


from config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    JWT_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    JWT_REFRESH_SECRET_KEY,
)


def get_now_time() -> datetime.utcnow:
    return datetime.utcnow()


def create_token(subject: Union[str, Any], expires_delta: int = None, expired_value: int = 0, secret: str = "") -> str:
    expires_delta = (
        (get_now_time() + timedelta(minutes=expires_delta if expires_delta else expired_value))
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret, ALGORITHM)
    return encoded_jwt


create_access_token = partial(create_token, secret=JWT_SECRET_KEY, expired_value=ACCESS_TOKEN_EXPIRE_MINUTES)
create_refresh_token = partial(create_token, secret=JWT_REFRESH_SECRET_KEY, expired_value=REFRESH_TOKEN_EXPIRE_MINUTES)


def generate_image_name(old_name: str) -> str:
    # old_name = f.1.png
    # f.1.png -> ["f.1", "png"] -> rand_str.join ==> "f.1_3x5g.png
    rand_str = "_" + "".join(random.choice(string.ascii_letters) for _ in range(8)) + "."  # `_3x5g.`
    new = rand_str.join(old_name.rsplit(".", 1))
    return new


class PwdManager:
    pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, password: str):
        return cls.pwd_cxt.hash(password)

    @classmethod
    def verify(cls, hashed_password, plain_password):
        return cls.pwd_cxt.verify(plain_password, hashed_password)


def parse_args():
    parser = argparse.ArgumentParser(description='Run a ErpiGRAM backend application.')
    parser.add_argument("--reload", action="store_true", help="reload app on code update")
    parser.add_argument("--devmode", action="store_true", help="clean db and populate dummy data")
    return parser.parse_args()
