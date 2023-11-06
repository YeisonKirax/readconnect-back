from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import Engine, get_db_session
from config.environment import env_data
from readconnect.auth.infrastructure.routes.auth_routes import auth_router
from scripts.poblate_db import poblate_db
from shared.infrastructure.db.schemas.entity_meta_schema import EntityMeta

# set_up_json_logger()
app = FastAPI()
app.include_router(prefix="/v1", router=auth_router, tags=["Authentication"])


@app.on_event("startup")
async def init_tables():
    async with Engine.begin() as conn:
        # await conn.run_sync(EntityMeta.metadata.drop_all)
        await conn.run_sync(EntityMeta.metadata.create_all)


@app.get("/seed", tags=["Seed"], description="Load in db the example dataset")
async def seed(session: Annotated[AsyncSession, Depends(get_db_session)]):
    await poblate_db(session)
    return {"msg": "dataset loaded"}


def main():
    uvicorn.run(
        "src.main:app",
        host=env_data.host,
        port=env_data.port,
        reload=True,
        workers=2,
        # log_config=None,
        # use_colors=False,
    )


if __name__ == "__main__":
    main()
