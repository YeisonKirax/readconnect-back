from typing import List

from nanoid import generate
from pydantic import BaseModel


class Category(BaseModel):
    id: str = generate()
    name: str
    books: List | None = None
