from fastapi import APIRouter

router = APIRouter()


@router.get("/{id}", summary="Get all tasks", description="Retrieve a list of all tasks.")
def get_user_by_username(id: str):
    return {"taskid": id}
