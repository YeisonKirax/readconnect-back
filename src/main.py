import logging
import uvicorn
from fastapi import FastAPI

from config.environment import load_env, env_data
from config.logger import set_up_json_logger

load_env()
set_up_json_logger()
logging.info(env_data.get_json())

app = FastAPI()


@app.get("/")
async def get_hello():
    return {"msg": "Hello world!"}


def main():
    uvicorn.run(
        "src.main:app",
        host=env_data.DB_HOST,
        port=env_data.DB_PORT,
        reload=True,
        workers=2,
        log_config=None,
        use_colors=False,
    )


if __name__ == "__main__":
    main()
