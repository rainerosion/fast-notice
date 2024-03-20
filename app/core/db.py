import logging

from sqlmodel import Session, create_engine

from app.core.config import settings
from app.models import User # noqa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.info(str(settings.SQLALCHEMY_DATABASE_URI))

print(str(settings.SQLALCHEMY_DATABASE_URI))
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)


def init_db(session: Session) -> None:
    pass
