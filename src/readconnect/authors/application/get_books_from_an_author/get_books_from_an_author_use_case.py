from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from readconnect.authors.domain.services.authors_service import AuthorsService


@dataclass()
class GetBooksFromAnAuthorUseCase:
    authors_service: Annotated[AuthorsService, Depends(AuthorsService)]

    async def execute(self, author_id: str):
        author = await self.authors_service.get_book_from_author(author_id)
        return author
