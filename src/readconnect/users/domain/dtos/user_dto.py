from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    name: str
    surname: str
    email: str
    password: str
