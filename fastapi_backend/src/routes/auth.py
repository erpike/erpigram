import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import ValidationError

from config import JWT_SECRET_KEY, ALGORITHM
from src.models import db_proxy, User
from src.routes import db_session
from src.schemas import TokenSchema
from src.utils import PwdManager, create_access_token


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")
router = APIRouter(tags=["Authentication"])


@router.post(
    '/login',
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
    dependencies=[Depends(db_session)],
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if (user := User.get_or_none(username=form_data.username)) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    if not PwdManager.verify(user.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return dict(
        access_token=create_access_token(user.username),
        refresh_token=create_access_token(user.username),
        token_type="Bearer",
        username=user.username,
        user_id=user.id,
    )


def identify_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        with db_proxy:
            user = User.get_or_none(username=username)
            if not user:
                raise credentials_exception
    except (jwt.PyJWTError, ValidationError):
        raise credentials_exception
    return user
