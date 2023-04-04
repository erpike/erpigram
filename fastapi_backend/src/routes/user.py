from typing import List, Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.models import User
from src.routes import db_session
from src.routes.auth import identify_user
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
async def create_user(request: UserBase):
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


@router.get(
    "",
    response_description="List of users",
    response_model=List[UserDisplay],
    dependencies=[Depends(db_session)],
)
async def list_user(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    user: User = Depends(identify_user),
):
    """
    :return: list of existed users.\n
    `limit` and `offset` - standard SQL query parameters.
    """
    query = User.select().dicts()
    query = query.limit(limit) if limit else query
    query = query.offset(offset) if offset else query
    return list(query)
#