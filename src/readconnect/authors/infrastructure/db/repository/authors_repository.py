from typing import Annotated, List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db_session
from readconnect.authors.domain.models.author_model import Author
from readconnect.authors.infrastructure.db.entities.author_entity import AuthorEntity


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