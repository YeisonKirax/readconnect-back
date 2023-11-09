from pydantic import BaseModel


class BooksCategories(BaseModel):
    book_id: str
    category_id: str
