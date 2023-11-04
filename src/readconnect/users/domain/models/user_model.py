from nanoid import generate
from pydantic import BaseModel, EmailStr, SecretStr


class User(BaseModel):
    id: str = generate()
    avatar: str | None = None
    name: str
    surname: str
    email: EmailStr
    password: SecretStr
