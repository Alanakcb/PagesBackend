from pages.domain.repositories.review_repository import ReviewRepository
from pages.domain.entities.review import Review
from typing import List


class GetReviewsByUserUseCase:
    def __init__(self, repository: ReviewRepository):
        self.repository = repository

    async def execute(self, user_id: str) -> List[Review]:
        return await self.repository.get_reviews_by_user(user_id)
