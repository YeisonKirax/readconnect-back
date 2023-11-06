import json
from pathlib import Path
from typing import List, Tuple

from nanoid import generate
from sqlalchemy.ext.asyncio import AsyncSession

from readconnect.authors.infrastructure.db.entities.author_entity import (
    AuthorEntity,
    AuthorsBooksEntity,
)
from readconnect.books.infrastructure.db.entities.book_entity import (
    BookEntity,
    BooksCategoriesEntity,
)
from readconnect.categories.infrastructure.db.entities.category_entity import (
    CategoryEntity,
)


async def poblate_db(session: AsyncSession):
    script_location = Path(__file__).absolute().parent
    file_location = script_location / "amazon.books.json"

    with open(file_location) as user_file:
        parsed_json = json.load(user_file)
    books = parsed_json[:301]
    categories = []
    authors = []
    categories_books: List[Tuple[str, str]] = []
    authors_books: List[Tuple[str, str]] = []
    books_parsed: List[BookEntity] = []
    authors_parsed: List[AuthorEntity] = []
    categories_parsed: List[CategoryEntity] = []

    for book in books:
        book_id = generate()
        book_parsed = BookEntity(
            id=book_id,
            title=book["title"],
            isbn=book["isbn"] if "isbn" in book.keys() else "",
            page_count=book["pageCount"],
            published_date=book["publishedDate"]["$date"]
            if "publishedDate" in book.keys()
            else "",
            thumbnail_url=book["thumbnailUrl"] if "thumbnailUrl" in book.keys() else "",
            short_description=book["shortDescription"]
            if "shortDescription" in book.keys()
            else "",
            long_description=book["longDescription"]
            if "longDescription" in book.keys()
            else "",
            status=book["status"],
        )
        print(book_parsed.id)
        books_parsed.append(book_parsed)
        for tag in book["categories"]:
            tag_sanitized = str(tag).strip().lower()
            if tag_sanitized != "":
                if tag_sanitized not in categories:
                    category_id = generate()
                    category_parsed = CategoryEntity(
                        id=category_id, name=tag_sanitized.capitalize()
                    )
                    categories_books.append((category_parsed.id, book_parsed.id))
                    categories.append(tag_sanitized)
                    categories_parsed.append(category_parsed)
                    continue
                category_index = categories.index(tag_sanitized)
                categories_books.append(
                    (categories_parsed[category_index].id, book_parsed.id)
                )

        for author in book["authors"]:
            author_sanitized = str(author).strip().lower()
            if author_sanitized != "":
                if author_sanitized not in authors:
                    author_id = generate()
                    author_parsed = AuthorEntity(
                        id=author_id, name=author_sanitized.capitalize()
                    )
                    authors_books.append((author_parsed.id, book_parsed.id))
                    authors.append(author_sanitized)
                    authors_parsed.append(author_parsed)
                    continue
                author_index = authors.index(author_sanitized)
                authors_books.append((authors_parsed[author_index].id, book_parsed.id))

    categories_books_parsed: List[BooksCategoriesEntity] = [
        BooksCategoriesEntity(category_id=category[0], book_id=category[1])
        for category in categories_books
    ]
    authors_books_parsed: List[AuthorsBooksEntity] = [
        AuthorsBooksEntity(author_id=author_book[0], book_id=author_book[1])
        for author_book in authors_books
    ]
    session.add_all(books_parsed)
    await session.commit()
    session.add_all(authors_parsed)
    await session.commit()
    session.add_all(categories_parsed)
    await session.commit()
    session.add_all(categories_books_parsed)
    await session.commit()
    session.add_all(authors_books_parsed)
    await session.commit()
