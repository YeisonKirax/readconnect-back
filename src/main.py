from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from tortoise.contrib.fastapi import register_tortoise

from config.db import get_db_session
from config.environment import env_data
from readconnect.auth.infrastructure.routes.auth_routes import auth_router
from readconnect.authors.infrastructure.routes.authors_routes import authors_router
from readconnect.books.infrastructure.routes.books_routes import books_router
from readconnect.categories.infrastructure.db.entities.category_t_entity import (
    CategoryEntity,
)
from scripts.poblate_db import poblate_db
from shared.domain.dtos.query_params import QueryParams

# set_up_json_logger()
app = FastAPI()
app.include_router(prefix="/v1", router=auth_router, tags=["Authentication"])
app.include_router(prefix="/v1", router=authors_router, tags=["Authors"])
app.include_router(prefix="/v1", router=books_router, tags=["Books"])


# @app.on_event("startup")
# async def init_tables():
#     async with Engine.begin() as conn:
#         # await conn.run_sync(EntityMeta.metadata.drop_all)
#         await conn.run_sync(EntityMeta.metadata.create_all)


@app.get("/seed", tags=["Seed"], description="Load in db the example dataset")
async def seed(session: Annotated[AsyncSession, Depends(get_db_session)]):
    await poblate_db(session)
    return {"msg": "dataset loaded"}


@app.get("/")
async def home(params: QueryParams = Depends()):
    categories = await CategoryEntity.all()
    return categories


DATABASE_URL = f"postgres://{env_data.db_user}:{env_data.db_pass}@{env_data.db_host}:{env_data.db_port}/{env_data.db_name}"

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": [CategoryEntity.__module__]},
    generate_schemas=True,
    add_exception_handlers=True,
)


def main():
    uvicorn.run(
        "src.main:app",
        host=env_data.host,
        port=env_data.port,
        reload=True,
        workers=2,
        lifespan="on"
        # log_config=None,
        # use_colors=False,
    )


if __name__ == "__main__":
    main()
