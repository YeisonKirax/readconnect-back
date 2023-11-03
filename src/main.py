import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_hello():
    return {"msg": "Hello world!"}


def main():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True, workers=2)


if __name__ == "__main__":
    main()
