from nanoid import generate
from sqlalchemy import (
    String,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped

from readconnect.books.domain.models.restrictions import (
    BOOKS_CATEGORIES_TABLE_NAME,
)
from readconnect.categories.domain.models.category_model import Category
from readconnect.categories.domain.models.restrictions import CATEGORIES_TABLE_NAME
from readconnect.shared.infrastructure.db.schemas.entity_meta_schema import EntityMeta


class CategoryEntity(EntityMeta):
    __tablename__ = CATEGORIES_TABLE_NAME

    id: Mapped[str] = mapped_column(
        String(50), default=generate(), primary_key=True, unique=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    books = relationship(
        "BookEntity",
        secondary=BOOKS_CATEGORIES_TABLE_NAME,
        back_populates="categories",
        uselist=True,
        innerjoin=True,
        lazy="selectin",
    )

    def normalize(self) -> Category:
        return Category(
            id=self.id,
            name=self.name,
        )
