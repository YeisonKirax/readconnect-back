from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError

from readconnect.authors.application.get_authors.get_authors_use_case import (
    GetAuthorsUseCase,
)
from readconnect.authors.application.get_books_from_an_author.get_books_from_an_author_use_case import (
    GetBooksFromAnAuthorUseCase,
)
from readconnect.authors.domain.dtos.authors_query_params import AuthorsQueryParams
from readconnect.authors.domain.models.author_model import Author
from readconnect.shared.domain.dtos.error_response_dto import ErrorResponse
from readconnect.shared.domain.exceptions.exceptions import NotFoundError

authors_router = APIRouter(prefix="/authors")


@authors_router.get(
    "", status_code=200, response_model=List[Author], response_model_exclude_none=True
)
async def get_authors(
    get_authors_use_case: Annotated[GetAuthorsUseCase, Depends(GetAuthorsUseCase)],
    params: AuthorsQueryParams = Depends(),
):
    try:
        authors = await get_authors_use_case.execute(params)
        return authors
    except Exception as e:
        detail = f"Ocurrió un problema al realizar su petición. Detalle: {e.__str__()}"
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=jsonable_encoder({"details": detail, "status": "error"}),
        )


@authors_router.get(
    "/{author_id}",
    response_model_exclude_none=True,
    responses={
        200: {"model": Author},
        502: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def get_author(
    author_id: str,
    get_books_from_and_author_use_case: Annotated[
        GetBooksFromAnAuthorUseCase, Depends(GetBooksFromAnAuthorUseCase)
    ],
):
    try:
        authors = await get_books_from_and_author_use_case.execute(author_id)
        return authors
    except ValidationError as e:
        details = f"Ocurrió un problema al realizar su petición. Detalle: {e.__str__()}"
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(ErrorResponse(details=details)),
        )
    except NotFoundError as e:
        details = f"Ocurrió un problema al realizar su petición. Detalle: {e.details}"
        return JSONResponse(
            status_code=e.status_code,
            content=jsonable_encoder(ErrorResponse(details=details)),
        )
    except Exception as e:
        details = f"Ocurrió un problema al realizar su petición. Detalle: {e.__str__()}"
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=jsonable_encoder(ErrorResponse(details=details)),
        )
