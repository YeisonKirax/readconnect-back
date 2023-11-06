from nanoid import generate
from sqlalchemy import (
    Column,
    String,
)
from sqlalchemy.orm import relationship

from readconnect.books.domain.models.restrictions import (
    BOOKS_CATEGORIES_TABLE_NAME,
)
from readconnect.categories.domain.models.category_model import Category
from shared.infrastructure.db.schemas.entity_meta_schema import EntityMeta


class CategoryEntity(EntityMeta):
    __tablename__ = "categories"

    id = Column(String(50), default=generate(), primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    books = relationship(
        "BookEntity",
        secondary=BOOKS_CATEGORIES_TABLE_NAME,
        back_populates="categories",
    )

    def normalize(self) -> Category:
        return Category(
            id=self.id,
            name=self.name,
        )
