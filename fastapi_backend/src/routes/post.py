from fastapi import APIRouter, Depends, HTTPException, status
from peewee import IntegrityError

from src.models import Post
from src.routes import db_session
from src.schemas import PostBase, PostDisplay

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
def create_post(request: PostBase):
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
