class GetAllReviews:
    def __init__(self, review_repository):
        self.review_repository = review_repository

    async def execute(self) -> list:
        return await self.review_repository.get_all_reviews()
