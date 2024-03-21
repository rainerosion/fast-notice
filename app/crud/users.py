from sqlmodel import Session, select

from app.core.errors import ErrorCode
from app.core.security import get_password_hash, verify_password
from app.core.utils import ConditionUtils
from app.models.user import UserCreate, User


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create,
        update={"password": get_password_hash(user_create.password), "is_active": True, "is_superuser": False}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_by_username(*, session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user


def get_user_by_email(*, session: Session, email: str) -> User:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    ConditionUtils.must_not_empty(user, ErrorCode.USER_NOT_FOUND)
    return user


def authenticate(*, session: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(session=session, username=username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
