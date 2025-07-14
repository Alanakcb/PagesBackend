from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from pages.usecases.review.add_review import AddReviewUseCase
from pages.usecases.review.delete_review import DeleteReviewUseCase
from pages.usecases.review.get_review_by_book import GetReviewsByBookUseCase
from pages.usecases.review.get_review_by_user import GetReviewsByUserUseCase
from pages.domain.entities.review import Review
from pages.domain.entities.user import User
import uuid
from pages.api.schemas.review_schema import AddReviewInput, ReviewOutput
from pages.domain.repositories.review_repository import ReviewRepository
from sqlalchemy.ext.asyncio import AsyncSession
from pages.api.deps import (
    get_db_session,
    get_user_repository,
    get_review_repository,
    get_current_user,
)
from pages.infra.repositories.sqlalchemy.sqlalchemy_review_repository import (
    SQLAlchemyReviewRepository,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pages.api.schemas.review_schema import review_to_output, reviews_to_output

security = HTTPBearer()
router = APIRouter()


@router.get("/book/{book_id}", response_model=List[ReviewOutput])
async def get_reviews_by_book(
    book_id: str, review_repo: ReviewRepository = Depends(get_review_repository)
):
    usecase = GetReviewsByBookUseCase(review_repo)
    reviews = await usecase.execute(book_id)
    return reviews_to_output(reviews)


@router.get("/user", response_model=List[ReviewOutput])
async def get_reviews_by_user(
    review_repo: ReviewRepository = Depends(get_review_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: User = Depends(get_current_user),
):
    usecase = GetReviewsByUserUseCase(review_repo)
    reviews = await usecase.execute(user.id)
    return reviews_to_output(reviews)


@router.post("/", response_model=ReviewOutput)
async def add_review(
    data: AddReviewInput,
    review_repo: ReviewRepository = Depends(get_review_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: User = Depends(get_current_user),
):
    if data.date.tzinfo is not None:
        data.date = data.date.replace(tzinfo=None)
        review = Review(
            id=str(uuid.uuid4()),
            book_id=data.book_id,
            user_id=user.id,
            review=data.review,
            date=data.date,
        )
    usecase = AddReviewUseCase(review_repo)
    added_review = await usecase.execute(review)
    if not added_review:
        raise HTTPException(status_code=400, detail="Failed to addreview")
    return review_to_output(added_review)


@router.delete("/{review_id}")
async def delete_review(
    review_id: str, review_repo: ReviewRepository = Depends(get_review_repository)
):
    usecase = DeleteReviewUseCase(review_repo)
    success = await usecase.execute(review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}
