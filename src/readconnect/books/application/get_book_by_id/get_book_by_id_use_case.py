from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from readconnect.books.domain.services.books_service import BooksService
from readconnect.shared.domain.exceptions.exceptions import NotFoundError


@dataclass()
class GetBookByIdUseCase:
    books_service: Annotated[BooksService, Depends(BooksService)]

    async def execute(self, book_id: str):
        book = await self.books_service.get_book_by_id(book_id)
        print(book)
        if book is None:
            raise NotFoundError(
                details="el libro no fue encontrado en nuestros registros",
                status_code=404,
            )
        return book.normalize_with_extra()
