from typing import List

from nanoid import generate
from pydantic import BaseModel


class AuthorBook(BaseModel):
    author_id: str
    book_id: str


class Author(BaseModel):
    id: str = generate()
    name: str
    books: List | None = []
