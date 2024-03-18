from fastapi import APIRouter

from app.models.user import User
from app.schemas.user import UserDTO

router = APIRouter()


@router.get("/{username}", summary="Get users", description="Retrieve a list of users.")
def get_user_by_username(username: str):
    user = User(id=1, username=username, email="lm@rainss.cm", status=True)
    return user


@router.get("/info/{id}", status_code=200, response_model=UserDTO)
def get_user_i(id: str):
    user = User(id=1, username="rainerosion", email="lm@rainss.cm", status=True)
    return user
