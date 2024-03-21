from typing import Annotated

from fastapi import APIRouter

from app.api.deps import SessionDep

router = APIRouter()

# @router("access-token")
# def login_access_token(session: SessionDep, form_data: Annotated[Oauth2PasswordRequestForm, Depends()]) -> Token:
#     pass