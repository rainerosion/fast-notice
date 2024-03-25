from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlmodel import Session

from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.core.errors import ErrorCode
from app.core.exceptions import ExceptionUtil
from app.core.security import OAuth2PasswordBearer
from app.models import User
from app.models.jwt import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")


# async def get_auth_token(request: Request) -> str | None:
#     try:
#         return await reusable_oauth2(request)
#     except HTTPException as e:
#         ExceptionUtil.raise_business_exception(ErrorCode.USER_NOT_LOGGED_IN)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    token_data = {}
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        ExceptionUtil.raise_forbidden_exception(ErrorCode.USER_CREDENTIALS_INVALID)
    user = session.get(User, token_data.sub)
    if not user:
        ExceptionUtil.raise_business_exception(ErrorCode.USER_NOT_LOGGED_IN)
    if not user.is_active:
        ExceptionUtil.raise_business_exception(ErrorCode.USER_INACTIVE)
    return user  # noqa


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        ExceptionUtil.raise_business_exception(ErrorCode.USER_NOT_SUPERUSER)
    return current_user
