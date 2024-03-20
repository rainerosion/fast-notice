from sqlmodel import Session

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
