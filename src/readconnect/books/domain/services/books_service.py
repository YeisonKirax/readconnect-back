from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from readconnect.books.domain.dtos.books_query_params import BooksQueryParams
from readconnect.books.infrastructure.db.repository.books_repository import (
    BooksRepository,
)


@dataclass()
class BooksService:
    books_repository: Annotated[BooksRepository, Depends(BooksRepository)]

    async def get_books(self, query: BooksQueryParams):
        if query.search is not None:
            return await self.books_repository.search(query)
        p = await self.books_repository.find(query)
        return p

    async def get_book_by_id(self, book_id: str):
        r = await self.books_repository.find_by_id(book_id)
        return r
