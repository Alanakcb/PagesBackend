from pages.domain.repositories.review_repository import ReviewRepository
from pages.domain.entities.review import Review
from typing import List, Optional
import pytest


class InMemoryReviewRepository(ReviewRepository):
    def __init__(self):
        self._reviews = {}

    @pytest.mark.asyncio
    async def get_all_reviews(self) -> List[Review]:
        return list(self._reviews.values())

    @pytest.mark.asyncio
    async def get_reviews_by_book(self, book_id: str) -> List[Review]:
        return [c for c in self._reviews.values() if c.book_id == book_id]

    @pytest.mark.asyncio
    async def get_reviews_by_user(self, user_id: str) -> List[Review]:
        return [c for c in self._reviews.values() if c.user_id == user_id]

    @pytest.mark.asyncio
    async def add_review(self, review: Review) -> Review:
        self._reviews[review.id] = review
        return review

    async def update_review(self, review):
        self._reviews[review.id] = review
        return review

    @pytest.mark.asyncio
    async def delete_review(self, review_id: str) -> None:
        self._reviews.pop(review_id, None)
