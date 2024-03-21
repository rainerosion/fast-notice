from fastapi import APIRouter
from sqlmodel import select

from app.api.deps import SessionDep, CurrentUser
from app.core.errors import ErrorCode
from app.core.resp import Result
from app.core.utils import ConditionUtils
from app.crud import users
from app.models.user import User, UserCreate

router = APIRouter()


@router.post("/", response_model=User)
def create_user(*, session: SessionDep, user_create: UserCreate):
    user_in = users.create_user(session=session, user_create=user_create)
    return user_in


@router.get("/", summary="Get all users", response_model=Result[User])
def get_all_users(session: SessionDep, current_user: CurrentUser):
    statement = select(User)
    user_all = session.exec(statement).all()
    return user_all


@router.get("/me", summary="Get me", response_model=Result[User])
def get_me(current_user: CurrentUser):
    return Result[User].success(data=current_user)


@router.get("/{username}", summary="Get user by username", response_model=Result[User])
def get_user_by_username(username: str, session: SessionDep):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    ConditionUtils.must_not_empty(user, ErrorCode.USER_NOT_FOUND)
    return Result[User].success(data=user)
