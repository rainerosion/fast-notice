from fastapi import APIRouter
from sqlmodel import select

from app.api.deps import SessionDep
from app.core.exceptions import BusinessException
from app.core.resp import Result
from app.crud import users
from app.models.user import User, UserCreate

router = APIRouter()


@router.post("/", response_model=User)
def create_user(*, session: SessionDep, user_create: UserCreate):
    user_in = users.create_user(session=session, user_create=user_create)
    return user_in


@router.get("/{username}", summary="Get users", response_model=Result[User])
def get_user_by_username(username: str, session: SessionDep):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    # 判断用户非空返回，否则提示
    if not user:
        raise BusinessException(1001, "用户不存在")
    return Result[User].success(data=user)
