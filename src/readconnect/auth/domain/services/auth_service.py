from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends
from jose import jwt
from jose.constants import Algorithms
from passlib.context import CryptContext

from config.environment import env_data
from readconnect.users.domain.models.user_model import User
from readconnect.users.infrastructure.db.repository.users_repository import (
    UsersRepository,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass()
class AuthService:
    users_repository: Annotated[UsersRepository, Depends(UsersRepository)]

    async def get_user_by_email(self, email: str):
        user = await self.users_repository.find_by_email(email)
        return user

    def create_new_user(self, user: User):
        return self.users_repository.create(user)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def generate_jwt(claims: dict):
        token = jwt.encode(
            claims=claims,
            key=env_data.secret_key,
            algorithm=Algorithms.HS512,
        )
        return token
