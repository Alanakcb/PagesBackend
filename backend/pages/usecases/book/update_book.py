from pages.domain.entities.book import Book
from pages.domain.repositories.book_repository import BookRepository
from typing import Optional


class UpdateBookUseCase:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def execute(self, book: Book) -> Optional[Book]:
        return await self.repository.update(book)
