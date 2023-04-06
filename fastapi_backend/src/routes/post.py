import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from peewee import IntegrityError

from src.models import Post, User
from src.routes import db_session
from src.routes.auth import identify_user
from src.schemas import PostBase, PostDisplay, UserDisplay

router = APIRouter(
    prefix="/post",
    tags=["Post"],
)

image_url_types = ["absolute", "relative"]


@router.post(
    "",
    response_model=PostDisplay,
    dependencies=[Depends(db_session)],
)
async def create_post(request: PostBase, current_user: UserDisplay = Depends(identify_user)):
    if request.image_url_type not in image_url_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parameter 'image_url_type' should be either 'absolute' or 'relative",
        )

    try:
        return Post.create(
            image_url=request.image_url,
            image_url_type=request.image_url_type,
            caption=request.caption,
            user=request.user_id,
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "",
    response_description="List of posts",
    response_model=List[PostDisplay],
    dependencies=[Depends(db_session)],
)
async def list_post(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
):
    """
    :return: list of existed users.\n
    `limit` and `offset` - standard SQL query parameters.
    """
    query = Post.select()
    query = query.limit(limit) if limit else query
    query = query.offset(offset) if offset else query
    return list(query)
