from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from readconnect.authors.domain.dtos.authors_query_params import AuthorsQueryParams
from readconnect.authors.domain.services.authors_service import AuthorsService


@dataclass()
class GetAuthorsUseCase:
    authors_service: Annotated[AuthorsService, Depends(AuthorsService)]

    async def execute(self, query: AuthorsQueryParams):
        authors = await self.authors_service.get_authors(query)
        return [author.normalize() for author in authors]
