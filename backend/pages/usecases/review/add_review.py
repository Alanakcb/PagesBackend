from pages.domain.entities.review import Review
from pages.domain.repositories.review_repository import ReviewRepository
from typing import Optional


class AddReviewUseCase:
    def __init__(self, repository: ReviewRepository):
        self.repository = repository

    async def execute(self, review: Review) -> Optional[Review]:
        return await self.repository.add_review(review)
