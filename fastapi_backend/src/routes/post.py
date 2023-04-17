import random
import shutil
import string
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from peewee import IntegrityError

from config import IMAGE_PATH, STATIC_DIRNAME, IMAGE_DIRNAME
from src.models import Post
from src.routes import db_session
from src.routes.auth import identify_user
from src.schemas import PostBase, PostDisplay, UserDisplay
from src.utils import generate_image_name

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


@router.post("/image")
async def upload_image(image: UploadFile = File()):
    # image.filename = f.1.png
    new_name = generate_image_name(image.filename)
    # f.1.png -> ["f.1", "png"] + new.join ==> "f.1_3x5g.png
    full_path = f"{STATIC_DIRNAME}/{IMAGE_DIRNAME}/{new_name}"

    with open(full_path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {"filename": full_path}
