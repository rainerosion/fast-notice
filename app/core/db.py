from sqlmodel import Session, create_engine

from app.core.config import settings
# from app.models imp

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    pass
