from fastapi import HTTPException
from sqlmodel import Session, select, or_

from app.core.errors import ErrorCode
from app.core.exceptions import ExceptionUtil
from app.core.security import get_password_hash, verify_password
from app.models.user import UserCreate, User, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    # 判断用户名是否存在
    user = get_user_by_user_or_email(session=session, username=user_create.username, email=user_create.email)
    if user:
        ExceptionUtil.raise_business_exception(ErrorCode.USER_ALREADY_EXISTS)
    db_obj = User.model_validate(
        user_create,
        update={"password": get_password_hash(user_create.password), "is_active": True, "is_superuser": False}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_by_user_or_email(*, session: Session, username: str, email: str) -> User | None:
    statement = select(User).where(or_(User.username == username, User.email == email))
    user = session.exec(statement).first()
    return user


def get_user_by_username(*, session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def update_user(*, session: Session, user_id: int, user_in: UserUpdate) -> User:
    # find user by id
    user = session.get(User, user_id)
    if not user:
        # raise HTTPException(status_code=404, detail="User not found")
        ExceptionUtil.raise_business_exception(ErrorCode.USER_NOT_FOUND)
    user_data = user_in.model_dump(exclude_unset=True)
    user_data["password"] = get_password_hash(user_data["password"])
    user.sqlmodel_update(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate(*, session: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(session=session, username=username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
