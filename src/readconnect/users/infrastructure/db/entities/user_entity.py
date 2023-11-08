from nanoid import generate
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from readconnect.shared.infrastructure.db.schemas.entity_meta_schema import EntityMeta
from readconnect.users.domain.models.user_model import User


class UserEntity(EntityMeta):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(50), default=generate(), primary_key=True, unique=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, default=None)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    avatar: Mapped[str] = mapped_column(String(2000), nullable=True, default="")
    password: Mapped[str] = mapped_column(String(2000), nullable=False)

    def normalize(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            surname=self.surname,
            email=self.email,
        )
