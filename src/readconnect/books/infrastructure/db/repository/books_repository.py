from dataclasses import dataclass
from typing import Annotated, List

from fastapi import Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db_session
from readconnect.books.domain.dtos.books_query_params import BooksQueryParams
from readconnect.books.domain.models.book_model import Book
from readconnect.books.infrastructure.db.entities.book_entity import BookEntity


@dataclass()
class BooksRepository:
    db: Annotated[AsyncSession, Depends(get_db_session)]

    async def create_many(self, new_books: List[Book]):
        books = [BookEntity(**book) for book in new_books]
        self.db.add_all(books)
        await self.db.commit()
        return books

    async def find_by_id(self, book_id: str) -> BookEntity:
        query = (
            select(BookEntity)
            .join(BookEntity.authors)
            .join(BookEntity.categories)
            .where(BookEntity.id == book_id)
        )
        result = await self.db.execute(query)
        return result.scalar()

    async def find(self, query: BooksQueryParams) -> Page[Book]:
        q = select(
            BookEntity.id,
            BookEntity.title,
            BookEntity.isbn,
            BookEntity.long_description,
            BookEntity.short_description,
            BookEntity.published_date,
            BookEntity.thumbnail_url,
            BookEntity.page_count,
            BookEntity.status,
        )
        if query.include_extra_data:
            q = select(BookEntity).join(BookEntity.authors).join(BookEntity.categories)
            return await paginate(self.db, q)

        return await paginate(self.db, q)

    async def search(self, query: BooksQueryParams) -> Page[Book]:
        q = select(
            BookEntity.id,
            BookEntity.title,
            BookEntity.isbn,
            BookEntity.long_description,
            BookEntity.short_description,
            BookEntity.published_date,
            BookEntity.thumbnail_url,
            BookEntity.page_count,
            BookEntity.status,
        ).filter(
            BookEntity.title.icontains(query.search)
            | BookEntity.isbn.icontains(query.search)
        )
        if query.include_extra_data:
            q = (
                select(BookEntity)
                .filter(
                    BookEntity.title.contains(query.search)
                    | BookEntity.isbn.contains(query.search)
                )
                .join(BookEntity.authors)
                .join(BookEntity.categories)
            )
            return await paginate(self.db, q)

        return await paginate(self.db, q)
