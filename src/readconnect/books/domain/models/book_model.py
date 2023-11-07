from typing import List

from nanoid import generate
from pydantic import BaseModel


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
    categories: List | None = None
    authors: List | None = None
