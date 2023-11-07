from typing import Annotated

from fastapi import APIRouter, Depends

from readconnect.authors.application.get_books_from_an_author.get_books_from_an_author_use_case import (
    GetBooksFromAnAuthorUseCase,
)
from readconnect.books.application.get_books.get_books_use_case import GetBooksUseCase
from readconnect.books.domain.dtos.books_query_params import BooksQueryParams

books_router = APIRouter(prefix="/books")


@books_router.get("", status_code=200)
async def get_books(
    get_books_use_case: Annotated[GetBooksUseCase, Depends(GetBooksUseCase)],
    params: BooksQueryParams = Depends(),
):
    try:
        books = await get_books_use_case.execute(params)
        return books
    except Exception as e:
        return {"status": "error", "message": e.__str__()}


@books_router.get("/{book_id}", status_code=200)
async def get_book_by_id(
    book_id: str,
    get_books_from_and_author_use_case: Annotated[
        GetBooksFromAnAuthorUseCase, Depends(GetBooksFromAnAuthorUseCase)
    ],
):
    try:
        books = await get_books_from_and_author_use_case.execute(book_id)
        return books
    except Exception as e:
        return {"status": "error", "message": e.__str__()}
