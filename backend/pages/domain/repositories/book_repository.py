from abc import ABC, abstractmethod
from pages.domain.entities.book import Book
from typing import Optional


class BookRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Book]:
        pass

    @abstractmethod
    async def get_by_id(self, book_id: str) -> Optional[Book]: ...

    @abstractmethod
    async def create(self, book: Book) -> Optional[Book]: ...

    @abstractmethod
    async def update(self, book: Book) -> Optional[Book]: ...

    @abstractmethod
    async def delete(self, book_id: str) -> None:
        pass
