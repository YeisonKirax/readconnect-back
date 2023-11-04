from pydantic import BaseModel


class SignupRequestDTO(BaseModel):
    name: str
    surname: str
    email: str
    password: str
