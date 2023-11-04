from nanoid import generate
from sqlalchemy import (
    Column,
    String,
)

from readconnect.users.domain.models.user_model import User
from shared.infrastructure.db.schemas.entity_meta_schema import EntityMeta


class UserEntity(EntityMeta):
    __tablename__ = "users"

    id = Column(String(50), default=generate(), primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    avatar = Column(String(2000), nullable=True)
    password = Column(String(2000), nullable=False)

    def normalize(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            surname=self.surname,
            email=self.email,
            avatar=self.avatar,
        )
