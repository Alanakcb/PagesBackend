from pages.domain.repositories.review_repository import ReviewRepository
from pages.domain.entities.review import Review
from typing import List


class UpdateReviewUseCase:
    def __init__(self, repository: ReviewRepository):
        self.repository = repository

    async def execute(self, review: Review) -> Review:
        return await self.repository.update_review(review)
