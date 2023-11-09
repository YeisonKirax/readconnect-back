from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_pagination import Page
from pydantic_core import ValidationError

from readconnect.books.application.get_book_by_id.get_book_by_id_use_case import (
    GetBookByIdUseCase,
)
from readconnect.books.application.get_books.get_books_use_case import GetBooksUseCase
from readconnect.books.domain.dtos.books_query_params import BooksQueryParams
from readconnect.books.domain.models.book_model import Book
from readconnect.shared.domain.dtos.error_response_dto import ErrorResponse
from readconnect.shared.domain.exceptions.exceptions import NotFoundError

books_router = APIRouter(prefix="/books")


@books_router.get(
    "",
    status_code=200,
    response_model=Page[Book],
    responses={200: {"model": Page[Book]}},
    response_model_exclude_none=True,
)
async def get_books(
    get_books_use_case: Annotated[GetBooksUseCase, Depends(GetBooksUseCase)],
    params: BooksQueryParams = Depends(),
):
    try:
        books = await get_books_use_case.execute(params)
        return books
    except Exception as e:
        print(e)
        detail = f"Ocurrió un problema al realizar su petición. Detalle: {e.__str__()}"
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=jsonable_encoder({"details": detail, "status": "error"}),
        )


@books_router.get(
    "/{book_id}",
    response_model_exclude_none=True,
    responses={
        200: {"model": Book},
        502: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def get_book_by_id(
    book_id: str,
    get_book_by_id_use_case: Annotated[GetBookByIdUseCase, Depends(GetBookByIdUseCase)],
):
    try:
        print(book_id)
        books = await get_book_by_id_use_case.execute(book_id)
        return books
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
