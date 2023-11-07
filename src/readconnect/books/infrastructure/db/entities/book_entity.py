from nanoid import generate
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from readconnect.authors.domain.models.restrictions import AUTHORS_BOOKS_TABLE_NAME
from readconnect.books.domain.models.book_model import Book
from readconnect.books.domain.models.books_categories_model import BooksCategories
from readconnect.books.domain.models.restrictions import (
    BOOK_TABLE_NAME,
    BOOKS_CATEGORIES_TABLE_NAME,
)
from shared.infrastructure.db.schemas.entity_meta_schema import EntityMeta


class BooksCategoriesEntity(EntityMeta):
    __tablename__ = BOOKS_CATEGORIES_TABLE_NAME

    book_id = Column(
        String(50), ForeignKey("books.id"), nullable=False, primary_key=True
    )
    category_id = Column(
        String(50), ForeignKey("categories.id"), nullable=False, primary_key=True
    )

    def normalize(self) -> BooksCategories:
        return BooksCategories(category_id=self.category_id, book_id=self.book_id)


class BookEntity(EntityMeta):
    __tablename__ = BOOK_TABLE_NAME

    id = Column(
        String(50), default=generate(), primary_key=True, unique=True, index=True
    )
    title = Column(String(100), nullable=False)
    isbn = Column(String(50), nullable=True, default="")
    page_count = Column(Integer, nullable=False)
    published_date = Column(String(100), nullable=False, default="")
    thumbnail_url = Column(String(200), nullable=True, default="")
    short_description = Column(String(2000), nullable=True, default="")
    long_description = Column(String(5000), nullable=True, default="")
    status = Column(String(20), nullable=False)
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
            authors=[au.normalize() for au in self.authors]
            if len(self.authors) > 0
            else None,
            categories=[ca.normalize() for ca in self.categories]
            if len(self.categories) > 0
            else None,
        )
