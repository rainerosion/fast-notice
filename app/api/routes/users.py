from fastapi import APIRouter, Depends
from sqlmodel import select

from app.api.deps import SessionDep, CurrentUser, get_current_user
from app.core.errors import ErrorCode
from app.core.resp import Result
from app.core.utils import ConditionUtils
from app.crud import users
from app.models.user import User, UserCreate, UserUpdate, UserOut

router = APIRouter()


@router.post("/", response_model=Result[UserOut])
def create_user(*, session: SessionDep, user_create: UserCreate):
    user_in = users.create_user(session=session, user_create=user_create)
    return Result[UserOut].success(data=user_in)


@router.get(
    "/",
    summary="Get all users",
    dependencies=[Depends(get_current_user)],
    response_model=Result[list[UserOut]]
)
def get_all_users(session: SessionDep):
    statement = select(User)
    user_all = session.exec(statement).all()
    return Result[list[UserOut]].success(data=user_all)


@router.patch("/{user_id}", response_model=Result[UserOut])
def update_user(*, session: SessionDep, user_id: int, user_in: UserUpdate):
    user = users.update_user(session=session, user_id=user_id, user_in=user_in)
    return Result[UserOut].success(data=user)


@router.get("/me", summary="Get me", response_model=Result[UserOut])
def get_me(current_user: CurrentUser):
    return Result[UserOut].success(data=current_user)


@router.get("/{username}", summary="Get user by username", response_model=Result[UserOut])
def get_user_by_username(username: str, session: SessionDep):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    ConditionUtils.must_not_empty(user, ErrorCode.USER_NOT_FOUND)
    return Result[UserOut].success(data=user)
