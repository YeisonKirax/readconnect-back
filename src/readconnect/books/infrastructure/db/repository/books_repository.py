from typing import Annotated, List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db_session
from readconnect.books.domain.models.book_model import Book
from readconnect.books.infrastructure.db.entities.book_entity import BookEntity


class BooksRepository:
    db: Annotated[AsyncSession, Depends(get_db_session)]

    async def create_many(self, new_books: List[Book]):
        books = [BookEntity(**book) for book in new_books]
        self.db.add_all(books)
        await self.db.commit()
        return books

    async def find_by_id(self, book_id: str):
        query = select(BookEntity).where(BookEntity.id == book_id)
        result = await self.db.execute(query)
        return result.scalar()
