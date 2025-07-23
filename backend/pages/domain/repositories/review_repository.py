from abc import ABC, abstractmethod
from pages.domain.entities.review import Review


class ReviewRepository(ABC):

    @abstractmethod
    async def get_all_reviews(self) -> list[Review]: ...

    @abstractmethod
    async def get_reviews_by_book(self, book_id: str) -> list[Review]: ...

    @abstractmethod
    async def get_reviews_by_user(self, user_id: str) -> list[Review]: ...

    @abstractmethod
    async def add_review(self, review: Review) -> Review: ...

    @abstractmethod
    async def update_review(self, review: Review) -> Review: ...

    @abstractmethod
    async def delete_review(self, review_id: str) -> None: ...
