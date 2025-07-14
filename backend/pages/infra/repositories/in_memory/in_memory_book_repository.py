from pages.domain.repositories.book_repository import BookRepository
from pages.domain.entities.book import Book
from typing import List, Optional
import pytest


class InMemoryBookRepository(BookRepository):
    def __init__(self):
        self._books = {}

    @pytest.mark.asyncio
    async def get_all(self) -> List[Book]:
        return list(self._books.values())

    @pytest.mark.asyncio
    async def get_by_id(self, book_id: str) -> Optional[Book]:
        return self._books.get(book_id)

    @pytest.mark.asyncio
    async def create(self, book: Book) -> Optional[Book]:
        self._books[book.id] = book
        return book

    @pytest.mark.asyncio
    async def update(self, book: Book) -> Optional[Book]:
        if book.id in self._books:
            self._books[book.id] = book
            return book
        return None

    @pytest.mark.asyncio
    async def delete(self, book_id: str) -> None:
        self._books.pop(book_id, None)
