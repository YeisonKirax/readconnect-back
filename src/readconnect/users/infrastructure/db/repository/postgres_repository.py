from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from readconnect.users.domain.models.user_model import User
from readconnect.users.infrastructure.db.entities.user_entity import UserEntity
from src.config.db import get_db_connection


@dataclass()
class PostgresRepository:
    db: Annotated[Session, Depends(get_db_connection)]

    def create(self, new_user: User):
        user = UserEntity(
            id=new_user.id,
            avatar=new_user.avatar,
            name=new_user.name,
            surname=new_user.surname,
            email=new_user.email,
            password=new_user.password.get_secret_value(),
        )
        self.db.add_all()
        self.db.commit()
        return user

    def find_by_id(self, user_id: str):
        return self.db.get(UserEntity, {"id": user_id})

    def find_by_email(self, email: str):
        return self.db.query(UserEntity).filter_by(email=email).first()
