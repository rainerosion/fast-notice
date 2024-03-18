from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    id: int
    username: str
    email: EmailStr
    status: bool = None

