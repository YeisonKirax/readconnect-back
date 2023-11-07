from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from readconnect.books.domain.dtos.books_query_params import BooksQueryParams
from readconnect.books.domain.services.books_service import BooksService


@dataclass()
class GetBooksUseCase:
    books_service: Annotated[BooksService, Depends(BooksService)]

    async def execute(self, query: BooksQueryParams):
        books = await self.books_service.get_books(query)
        if query.include_extra_data:
            return [
                book.normalize_with_extra().model_dump(exclude_none=True)
                for book in books
            ]

        return [book.normalize().model_dump(exclude_none=True) for book in books]
