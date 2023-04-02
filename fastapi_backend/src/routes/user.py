import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import ValidationError
from starlette import status

from config import JWT_SECRET_KEY, ALGORITHM
from src.models import db_proxy, User
from src.routes import db_session
from src.schemas import UserDisplay, UserBase, TokenSchema
from src.utils import PwdManager, create_access_token


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/token")
router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post(
    "/signup",
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


@router.post(
    '/login',
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
    dependencies=[Depends(db_session)]
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.get_or_none(username=form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    if not PwdManager.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return dict(
        access_token=create_access_token(user.username),
        refresh_token=create_access_token(user.username),
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
