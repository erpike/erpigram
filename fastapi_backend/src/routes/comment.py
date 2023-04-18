from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.models import Post, Comment, User
from src.routes import db_session
from src.routes.auth import identify_user
from src.schemas import CommentBase, CommentDisplay, UserDisplay


router = APIRouter(
    prefix="/comment",
    tags=["Comment"],
)


@router.post(
    "",
    response_model=CommentDisplay,
    dependencies=[Depends(db_session)],
)
async def create_comment(request: CommentBase, current_user: UserDisplay = Depends(identify_user)):
    if (
        not (post := Post.get_or_none(id=request.post_id))
        or not User.get_or_none(id=request.user_id)
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Either of parameter `post_id` / `user_id` is invalid (Does not exist).",
        )
    return Comment.create(
        post=post,
        text=request.text,
        user=request.user_id,
    )


@router.get(
    "/all/{post_id}",
    dependencies=[Depends(db_session)],
    response_model=List[CommentDisplay],
)
async def list_comments(post_id: int):
    post = Post.get_or_none(id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with specified id[{post_id}] was not found."
        )

    return list(Comment.select().where(Comment.post == post))
