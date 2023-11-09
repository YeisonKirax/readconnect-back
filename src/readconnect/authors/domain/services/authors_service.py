from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from readconnect.authors.domain.dtos.authors_query_params import AuthorsQueryParams
from readconnect.authors.infrastructure.db.repository.authors_repository import (
    AuthorsRepository,
)


@dataclass()
class AuthorsService:
    authors_repository: Annotated[AuthorsRepository, Depends(AuthorsRepository)]

    async def get_authors(self, query: AuthorsQueryParams):
        r = await self.authors_repository.find(query)
        return r

    async def get_book_from_author(self, author_id: str):
        r = await self.authors_repository.find_by_id(author_id)
        return r
