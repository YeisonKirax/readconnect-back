from typing import Annotated

from fastapi import APIRouter, Depends

from readconnect.authors.application.get_authors.get_authors_use_case import (
    GetAuthorsUseCase,
)
from readconnect.authors.domain.dtos.authors_query_params import AuthorsQueryParams

authors_router = APIRouter(prefix="/authors")


@authors_router.get("", status_code=200)
async def get_authors(
    get_authors_use_case: Annotated[GetAuthorsUseCase, Depends(GetAuthorsUseCase)],
    params: AuthorsQueryParams = Depends(),
):
    try:
        authors = await get_authors_use_case.execute(params)
        return authors
    except Exception as e:
        return {"status": "error", "message": e.__str__()}
