from pydantic import BaseModel


class QueryParams(BaseModel):
    page: int | None = None
    size: int | None = None
