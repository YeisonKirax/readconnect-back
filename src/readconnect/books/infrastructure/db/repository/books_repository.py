from dataclasses import dataclass
from typing import Annotated, List

from fastapi import Depends
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

    async def find_by_id(self, book_id: str):
        query = (
            select(BookEntity)
            .join(BookEntity.authors)
            .join(BookEntity.categories)
            .where(BookEntity.id == book_id)
        )
        result = await self.db.execute(query)
        return result.scalar()

    async def find(self, query: BooksQueryParams) -> List[BookEntity]:
        if query.page is not None and query.size is not None:
            q = (
                select(
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
                .limit(query.size)
                .offset((query.page - 1) * query.size)
            )
            if query.include_extra_data:
                q = (
                    select(BookEntity)
                    .join(BookEntity.authors)
                    .join(BookEntity.categories)
                    .limit(query.size)
                    .offset((query.page - 1) * query.size)
                )
                result = await self.db.execute(q)
                return result.scalars().all()
            result = await self.db.execute(q)
            result_mapped = result.mappings().fetchall()
            return [BookEntity(**book) for book in result_mapped]
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
            result = await self.db.execute(q)
            return result.scalars().all()
        result = await self.db.execute(q)
        result_mapped = result.mappings().fetchall()
        return [BookEntity(**book) for book in result_mapped]
