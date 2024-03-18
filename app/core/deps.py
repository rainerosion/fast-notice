from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session


def get_db() -> Generator[Session, None, None]:
    with Session() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
