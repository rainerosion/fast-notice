from fastapi import APIRouter

from app.api.routes import users, tasks, tests

router = APIRouter()


# api_router.include_router(login.router, tags=["login"])
@router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}


router.include_router(tests.router, prefix="/tests", tags=["test"])
router.include_router(users.router, prefix="/user", tags=["users"])
router.include_router(tasks.router, prefix="/task", tags=["tasks"])
