from fastapi import APIRouter

from app.api.deps import SessionDep
from app.crud import users
from app.models.user import User, UserCreate

router = APIRouter()

@router.post("/", response_model=User)
def create_user(*, session: SessionDep, user_create: UserCreate):
    user_in = users.create_user(session=session, user_create=user_create)
    return user_in


@router.get("/{username}", summary="Get users", description="Retrieve a list of users.")
def get_user_by_username(username: str):
    user = User(id=1, username=username, email="lm@rainss.cm", status=True)
    return user


@router.get("/info/{id}", status_code=200, response_model=User)
def get_user_i(id: str):
    user = User(id=1, username="rainerosion", email="lm@rainss.cm", status=True)
    return user
