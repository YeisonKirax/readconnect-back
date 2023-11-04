from pydantic import BaseModel


class LoginResponseDTO(BaseModel):
    token: str
