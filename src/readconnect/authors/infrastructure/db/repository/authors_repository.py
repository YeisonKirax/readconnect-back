from dataclasses import dataclass
from typing import Annotated, List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db_session
from readconnect.authors.domain.dtos.authors_query_params import AuthorsQueryParams
from readconnect.authors.infrastructure.db.entities.author_entity import (
    AuthorEntity,
)
from readconnect.books.infrastructure.db.entities.book_entity import BookEntity


@dataclass()
class AuthorsRepository:
    db: Annotated[AsyncSession, Depends(get_db_session)]

    async def find_by_id(self, author_id: str):
        print(author_id)
        query = (
            select(AuthorEntity)
            .join(AuthorEntity.books)
            .where(AuthorEntity.id == author_id)
        )
        result = await self.db.execute(query)
        return result.scalar()

    async def find(self, query: AuthorsQueryParams) -> List[AuthorEntity]:
        if query.page is not None and query.size is not None:
            q = (
                select(AuthorEntity.id, AuthorEntity.name)
                .limit(query.size)
                .offset((query.page - 1) * query.size)
            )
            if query.include_books:
                q = (
                    select(AuthorEntity)
                    .join(AuthorEntity.books)
                    .limit(query.size)
                    .offset((query.page - 1) * query.size)
                )
                result = await self.db.execute(q)
                return [a for a in result.scalars().all()]
            result = await self.db.execute(q)
            result_mapped = result.mappings().fetchall()
            return [AuthorEntity(**author) for author in result_mapped]
        q = select(AuthorEntity.id, AuthorEntity.name)
        if query.include_books:
            q = select(AuthorEntity).join(AuthorEntity.books)
            result = await self.db.execute(q)
            return [a for a in result.scalars().all()]
        result = await self.db.execute(q)
        result_mapped = result.mappings().fetchall()
        return [AuthorEntity(**author) for author in result_mapped]

    async def find_books(self, author_id: str) -> List[BookEntity]:
        q = (
            select(BookEntity)
            .join(BookEntity.authors)
            .where(AuthorEntity.id == author_id)
        )
        result = await self.db.execute(q)
        return [b for b in result.scalars().all()]
