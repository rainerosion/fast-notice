from sqlmodel import Session, select

from app.core.exceptions import BusinessException
from app.core.security import get_password_hash
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


def get_user_by_username(*, session: Session, username: str) -> User:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if not user:
        raise BusinessException(1001, "用户不存在")
    return user
