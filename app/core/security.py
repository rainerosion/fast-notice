from datetime import timedelta, datetime
from typing import Any, Dict, Optional, cast

from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from passlib.context import CryptContext
from starlette.requests import Request
from typing_extensions import Annotated, Doc  # type: ignore [attr-defined]

from app.core.config import settings
from app.core.errors import ErrorCode
from app.core.exceptions import ExceptionUtil

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    verify password
    :param plain_password: original password
    :param hashed_password: hashed password
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class OAuth2PasswordBearer(OAuth2):
    """
    OAuth2 flow for authentication using a bearer token obtained with a password.
    An instance of it would be used as a dependency.

    Read more about it in the
    [FastAPI docs for Simple OAuth2 with Password and Bearer](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/).
    """

    def __init__(
            self,
            tokenUrl: Annotated[
                str,
                Doc(
                    """
                    The URL to obtain the OAuth2 token. This would be the *path operation*
                    that has `OAuth2PasswordRequestForm` as a dependency.
                    """
                ),
            ],
            scheme_name: Annotated[
                Optional[str],
                Doc(
                    """
                    Security scheme name.
    
                    It will be included in the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            scopes: Annotated[
                Optional[Dict[str, str]],
                Doc(
                    """
                    The OAuth2 scopes that would be required by the *path operations* that
                    use this dependency.
                    """
                ),
            ] = None,
            description: Annotated[
                Optional[str],
                Doc(
                    """
                    Security scheme description.
    
                    It will be included in the generated OpenAPI (e.g. visible at `/docs`).
                    """
                ),
            ] = None,
            auto_error: Annotated[
                bool,
                Doc(
                    """
                    By default, if no HTTP Auhtorization header is provided, required for
                    OAuth2 authentication, it will automatically cancel the request and
                    send the client an error.
    
                    If `auto_error` is set to `False`, when the HTTP Authorization header
                    is not available, instead of erroring out, the dependency result will
                    be `None`.
    
                    This is useful when you want to have optional authentication.
    
                    It is also useful when you want to have authentication that can be
                    provided in one of multiple optional ways (for example, with OAuth2
                    or in a cookie).
                    """
                ),
            ] = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password=cast(Any, {"tokenUrl": tokenUrl, "scopes": scopes})
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                ExceptionUtil.raise_business_exception(ErrorCode.USER_NOT_LOGGED_IN)
            else:
                return None
        return param
