from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import SessionDep
from app.core import security
from app.core.config import settings
from app.core.errors import ErrorCode
from app.core.exceptions import ExceptionUtil
from app.core.utils import ConditionUtils
from app.crud import users
from app.models.jwt import Token

router = APIRouter()


@router.post("/access-token")
def login_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = users.authenticate(session=session, username=form_data.username, password=form_data.password)
    ConditionUtils.must_not_empty(user, ErrorCode.USER_LOGIN_FAILED)
    if not user.is_active:
        ExceptionUtil.raise_business_exception(ErrorCode.USER_INACTIVE)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(user.id, expires_delta=access_token_expires)
    return Token(access_token=token)
