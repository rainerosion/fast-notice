from fastapi import APIRouter

from app.api.routes import users, login

router = APIRouter()


# api_router.include_router(login.router, tags=["login"])
@router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Server Worked!"}


router.include_router(login.router, prefix="/login", tags=["login"])
router.include_router(users.router, prefix="/user", tags=["users"])
