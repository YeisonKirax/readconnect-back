from nanoid import generate
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from readconnect.authors.domain.models.author_model import Author, AuthorBook
from readconnect.authors.domain.models.restrictions import (
    AUTHORS_BOOKS_TABLE_NAME,
    AUTHOR_TABLE_NAME,
)
from shared.infrastructure.db.schemas.entity_meta_schema import EntityMeta


class AuthorsBooksEntity(EntityMeta):
    __tablename__ = AUTHORS_BOOKS_TABLE_NAME

    author_id = Column(
        String(50),
        ForeignKey("authors.id"),
        nullable=False,
        primary_key=True,
    )
    book_id = Column(
        String(50),
        ForeignKey("books.id"),
        nullable=False,
        primary_key=True,
    )

    def normalize(self) -> AuthorBook:
        return AuthorBook(author_id=self.author_id, book_id=self.book_id)


class AuthorEntity(EntityMeta):
    __tablename__ = AUTHOR_TABLE_NAME

    id = Column(String(50), default=generate(), primary_key=True, unique=True)
    name = Column(String(100), nullable=False)
    books = relationship(
        "BookEntity",
        secondary=AUTHORS_BOOKS_TABLE_NAME,
        back_populates="authors",
        uselist=True,
        innerjoin=True,
        lazy="selectin",
    )

    def normalize(self) -> Author:
        if len(self.books) > 0:
            return Author(
                id=self.id,
                name=self.name,
                books=[book.normalize() for book in self.books],
            )
        print(self.books)
        return Author(id=self.id, name=self.name, books=[])
