from typing import Annotated

from fastapi import APIRouter, Depends

from readconnect.authors.application.get_authors.get_authors_use_case import (
    GetAuthorsUseCase,
)
from readconnect.authors.application.get_books_from_an_author.get_books_from_an_author_use_case import (
    GetBooksFromAnAuthorUseCase,
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


@authors_router.get("/{author_id}/books", status_code=200)
async def get_books_authors(
    author_id: str,
    get_books_from_and_author_use_case: Annotated[
        GetBooksFromAnAuthorUseCase, Depends(GetBooksFromAnAuthorUseCase)
    ],
):
    try:
        authors = await get_books_from_and_author_use_case.execute(author_id)
        return authors
    except Exception as e:
        return {"status": "error", "message": e.__str__()}
