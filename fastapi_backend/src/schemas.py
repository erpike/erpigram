from datetime import datetime
from typing import List, Any

from peewee import ModelSelect
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        return res


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class RefreshTokenSchema(BaseModel):
    token: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    username: str
    user_id: int


class PostBase(BaseModel):
    image_url: str
    image_url_type: str  # relative or absolute
    caption: str
    user_id: int


class CommentBase(BaseModel):
    user_id: int
    post_id: int
    text: str

    class Config:
        orm_mode = True


class UserPostDisplay(BaseModel):
    username: str

    class Config:
        orm_mode = True


# for Post display
class CommentDisplay(BaseModel):
    id: int
    text: str
    user: UserPostDisplay
    timestamp: datetime

    class Config:
        orm_mode = True


class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: UserPostDisplay
    comments: List[CommentDisplay]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
