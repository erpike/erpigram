from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class PostBase(BaseModel):
    image_url: str
    image_url_type: str  # relative or absolute
    caption: str
    user_id: int


class UserPostDisplay(BaseModel):
    username: str

    class Config:
        orm_mode = True


class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: UserPostDisplay

    class Config:
        orm_mode = True
