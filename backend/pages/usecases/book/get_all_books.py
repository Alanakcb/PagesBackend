from pages.domain.repositories.book_repository import BookRepository
from pages.domain.entities.book import Book
from typing import List


class GetAllBooksUseCase:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def execute(self) -> List[Book]:
        return await self.repository.get_all()
