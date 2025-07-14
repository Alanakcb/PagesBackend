from pages.domain.repositories.review_repository import ReviewRepository


class DeleteReviewUseCase:
    def __init__(self, repository: ReviewRepository):
        self.repository = repository

    async def execute(self, review_id: str) -> bool:
        await self.repository.delete_review(review_id)
        return True
