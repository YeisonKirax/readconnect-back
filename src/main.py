import uvicorn
from fastapi import FastAPI

from config.environment import env_data
from readconnect.auth.infrastructure.routes.auth_routes import auth_router
from shared.infrastructure.db.schemas.entity_meta_schema import init

# set_up_json_logger()
app = FastAPI()
app.include_router(prefix="/v1", router=auth_router, tags=["Authentication"])

init()


@app.get("/")
async def get_hello():
    return {"msg": "Hello world!"}


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
