from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pages.domain.entities.review import Review
from pages.domain.repositories.review_repository import ReviewRepository
from pages.infra.models.review_model import ReviewModel
from pages.infra.models.book_model import BookModel
from sqlalchemy.orm import joinedload


class SQLAlchemyReviewRepository(ReviewRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_reviews_by_book(self, book_id: str) -> List[Review]:
        result = await self._session.execute(
            select(ReviewModel)
            .options(joinedload(ReviewModel.user))
            .where(ReviewModel.book_id == book_id)
        )
        return [c.to_entity() for c in result.unique().scalars().all()]

    async def get_reviews_by_user(self, user_id: str) -> List[Review]:
        result = await self._session.execute(
            select(ReviewModel).where(ReviewModel.user_id == user_id)
        )
        return [c.to_entity() for c in result.unique().scalars().all()]

    async def add_review(self, review: Review) -> Review:
        stmt = select(BookModel).where(BookModel.id == str(review.book_id))
        result = await self._session.execute(stmt)
        book = result.unique().scalar_one_or_none()
        if not book:
            raise ValueError("Book not found for the givenreview")
        db_review = ReviewModel.from_entity(review)
        self._session.add(db_review)
        await self._session.commit()
        await self._session.refresh(db_review)
        return db_review.to_entity()

    async def delete_review(self, review_id: str) -> None:
        await self._session.execute(
            delete(ReviewModel).where(ReviewModel.id == review_id)
        )
        await self._session.commit()
