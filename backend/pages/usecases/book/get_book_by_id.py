from pages.domain.repositories.book_repository import BookRepository
from pages.domain.entities.book import Book
from typing import Optional


class GetBookByIdUseCase:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def execute(self, book_id: str) -> Optional[Book]:
        return await self.repository.get_by_id(book_id)
