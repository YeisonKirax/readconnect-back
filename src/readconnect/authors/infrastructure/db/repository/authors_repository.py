from dataclasses import dataclass
from typing import Annotated, List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db_session
from readconnect.authors.domain.dtos.authors_query_params import AuthorsQueryParams
from readconnect.authors.domain.models.author_model import Author
from readconnect.authors.infrastructure.db.entities.author_entity import (
    AuthorEntity,
)


@dataclass()
class AuthorsRepository:
    db: Annotated[AsyncSession, Depends(get_db_session)]

    async def create_many(self, new_authors: List[Author]):
        authors = [
            AuthorEntity(
                id=author.id,
                name=author.name,
            )
            for author in new_authors
        ]

        self.db.add_all(authors)
        await self.db.commit()
        return authors

    async def find_by_id(self, author_id: str):
        query = select(AuthorEntity).where(AuthorEntity.id == author_id)
        result = await self.db.execute(query)
        return result.scalar()

    async def find(self, query: AuthorsQueryParams) -> List[AuthorEntity]:
        if query.page is not None and query.size is not None:
            q = (
                select(AuthorEntity.id, AuthorEntity.name)
                .limit(query.size)
                .offset(query.page * query.size)
            )
            if query.include_books:
                q = select(AuthorEntity).join(AuthorEntity.books)
                result = await self.db.execute(q)
                return result.scalars().all()
            result = await self.db.execute(q)
            result_mapped = result.mappings().fetchall()
            return [AuthorEntity(**author) for author in result_mapped]
        q = select(AuthorEntity.id, AuthorEntity.name)
        if query.include_books:
            q = select(AuthorEntity).join(AuthorEntity.books)
            result = await self.db.execute(q)
            return result.scalars().all()
        result = await self.db.execute(q)
        result_mapped = result.mappings().fetchall()
        return [AuthorEntity(**author) for author in result_mapped]
