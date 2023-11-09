from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from readconnect.authors.domain.models.restrictions import AUTHORS_BOOKS_TABLE_NAME
from readconnect.books.domain.models.book_model import Book
from readconnect.books.domain.models.books_categories_model import BooksCategories
from readconnect.books.domain.models.restrictions import (
    BOOK_TABLE_NAME,
    BOOKS_CATEGORIES_TABLE_NAME,
)
from readconnect.shared.infrastructure.db.schemas.entity_meta_schema import EntityMeta


class BooksCategoriesEntity(EntityMeta):
    __tablename__ = BOOKS_CATEGORIES_TABLE_NAME

    book_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("books.id"), nullable=False, primary_key=True
    )
    category_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("categories.id"), nullable=False, primary_key=True
    )

    def normalize(self) -> BooksCategories:
        return BooksCategories(category_id=self.category_id, book_id=self.book_id)


class BookEntity(EntityMeta):
    __tablename__ = BOOK_TABLE_NAME

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    isbn: Mapped[str] = mapped_column(String(50), nullable=True, default="")
    page_count: Mapped[int] = mapped_column(Integer, nullable=False)
    published_date: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    thumbnail_url: Mapped[str] = mapped_column(String(200), nullable=True, default="")
    short_description: Mapped[str] = mapped_column(
        String(2000), nullable=True, default=""
    )
    long_description: Mapped[str] = mapped_column(
        String(5000), nullable=True, default=""
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    authors = relationship(
        "AuthorEntity",
        secondary=AUTHORS_BOOKS_TABLE_NAME,
        back_populates="books",
        innerjoin=True,
        uselist=True,
        lazy="selectin",
    )
    categories = relationship(
        "CategoryEntity",
        secondary=BOOKS_CATEGORIES_TABLE_NAME,
        back_populates="books",
        innerjoin=True,
        uselist=True,
        lazy="selectin",
    )

    def normalize(self) -> Book:
        return Book(
            id=self.id,
            title=self.title,
            isbn=self.isbn,
            page_count=self.page_count,
            published_date=self.published_date.__str__(),
            thumbnail_url=self.thumbnail_url,
            short_description=self.short_description,
            long_description=self.long_description,
            status=self.status,
            authors=None,
            categories=None,
        )

    def normalize_with_extra(self) -> Book:
        return Book(
            id=self.id,
            title=self.title,
            isbn=self.isbn,
            page_count=self.page_count,
            published_date=self.published_date.__str__(),
            thumbnail_url=self.thumbnail_url,
            short_description=self.short_description,
            long_description=self.long_description,
            status=self.status,
            authors=[au.normalize().model_dump() for au in self.authors]
            if len(self.authors) > 0
            else [],
            categories=[ca.normalize().model_dump() for ca in self.categories]
            if len(self.categories) > 0
            else [],
        )
