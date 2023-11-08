from nanoid import generate
from pydantic import BaseModel, EmailStr, SecretStr


class User(BaseModel):
    id: str = generate()
    avatar: str = ""
    name: str
    surname: str
    email: EmailStr
    password: SecretStr | None = None
