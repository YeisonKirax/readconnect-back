from pydantic import BaseModel


class SignupResponseDTO(BaseModel):
    status: str
    message: str
