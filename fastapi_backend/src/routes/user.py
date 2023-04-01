from fastapi import APIRouter, Depends

from src.models import db_proxy, User
from src.schemas import UserDisplay, UserBase
from src.utils import PwdManager

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


def db_session():
    with db_proxy:
        yield


@router.post("", response_model=UserDisplay, dependencies=[Depends(db_session)])
def create_user(request: UserBase):
    return User.create(
        username=request.username,
        email=request.email,
        password=PwdManager.hash(request.password),
    )
