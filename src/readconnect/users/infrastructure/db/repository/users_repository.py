from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from readconnect.users.domain.models.user_model import User
from readconnect.users.infrastructure.db.entities.user_entity import UserEntity
from src.config.db import get_db_session


@dataclass()
class UsersRepository:
    db: Annotated[AsyncSession, Depends(get_db_session)]

    async def create(self, new_user: User):
        user = UserEntity(
            id=new_user.id,
            avatar=new_user.avatar,
            name=new_user.name,
            surname=new_user.surname,
            email=new_user.email,
            password=new_user.password.get_secret_value(),
        )

        self.db.add(user)
        await self.db.commit()
        return user

    async def find_by_id(self, user_id: str):
        query = select(UserEntity).where(UserEntity.id == user_id)
        result = await self.db.execute(query)
        return result.scalar()

    async def find_by_email(self, email: str):
        query = select(UserEntity).where(UserEntity.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()
