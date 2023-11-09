from pydantic import BaseModel


class LoginResponseDTO(BaseModel):
    token: str
    user_id: str
    fullName: str
    avatar: str | None
