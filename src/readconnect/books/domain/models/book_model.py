from typing import List

from nanoid import generate
from pydantic import BaseModel


class Author(BaseModel):
    id: str
    name: str


class Category(BaseModel):
    id: str
    name: str


class Book(BaseModel):
    id: str = generate()
    title: str
    isbn: str = ""
    page_count: int
    published_date: str = ""
    thumbnail_url: str = ""
    short_description: str = ""
    long_description: str = ""
    status: str
    categories: List[Category] | None = None
    authors: List[Author] | None = None
