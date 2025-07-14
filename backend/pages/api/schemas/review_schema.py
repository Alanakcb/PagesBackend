from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from pages.api.schemas.user_schema import UserOutput
from pages.domain.entities.review import Review
from pages.api.schemas.user_schema import user_to_output


class AddReviewInput(BaseModel):
    book_id: str = Field(
        ..., description="ID do book ao qual o comentário será adicionado"
    )
    review: str = Field(
        ..., min_length=1, max_length=500, description="Texto do comentário"
    )
    date: datetime = Field(..., description="Data do comentário no formato ISO 8601")


class ReviewOutput(BaseModel):
    id: str = Field(..., description="ID do comentário")
    book_id: str = Field(..., description="ID do book ao qual o comentário pertence")
    user_id: str = Field(..., description="ID do usuário que fez o comentário")
    review: str = Field(
        ..., min_length=1, max_length=500, description="Texto do comentário"
    )
    date: datetime = Field(..., description="Data do comentário no formato ISO 8601")
    user: UserOutput = Field(..., description="Dados do usuário que está bookando")

    @classmethod
    def from_entity(cls, review):
        return cls(
            id=review.id,
            book_id=review.book_id,
            user_id=review.user_id,
            review=review.review,
            date=review.date,
            user=review.user,
        )


def review_to_output(review: Review) -> ReviewOutput:
    return ReviewOutput(
        id=review.id,
        book_id=review.book_id,
        user_id=review.user_id,
        review=review.review,
        date=review.date,
        user=user_to_output(review.user) if review.user else None,
    )


def reviews_to_output(reviews: list[Review]) -> list[ReviewOutput]:
    return [review_to_output(review) for review in reviews]
