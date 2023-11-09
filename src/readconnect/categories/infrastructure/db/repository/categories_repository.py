from typing import Annotated, List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db_session
from readconnect.categories.domain.models.category_model import Category
from readconnect.categories.infrastructure.db.entities.category_entity import (
    CategoryEntity,
)


class CategoriesRepository:
    db: Annotated[AsyncSession, Depends(get_db_session)]

    async def create_many(self, new_categories: List[Category]):
        categories = [
            CategoryEntity(
                id=category.id,
                name=category.name,
            )
            for category in new_categories
        ]

        self.db.add_all(categories)
        await self.db.commit()
        return categories

    async def find_by_id(self, category_id: str):
        query = select(CategoryEntity).where(CategoryEntity.id == category_id)
        result = await self.db.execute(query)
        return result.scalar()
