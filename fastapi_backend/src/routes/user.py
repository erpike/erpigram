from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.models import User
from src.routes import db_session
from src.schemas import UserDisplay, UserBase
from src.utils import PwdManager


router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post(
    "",
    response_model=UserDisplay,
    dependencies=[Depends(db_session)],
)
def create_user(request: UserBase):
    if User.get_or_none(username=request.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exist"
        )
    return User.create(
        username=request.username,
        email=request.email,
        password=PwdManager.hash(request.password),
    )
