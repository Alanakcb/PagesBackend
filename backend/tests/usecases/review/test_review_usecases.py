import uuid
import pytest
from pages.domain.entities.review import Review
from pages.infra.repositories.in_memory.in_memory_review_repository import (
    InMemoryReviewRepository,
)
from pages.usecases.review.add_review import AddReviewUseCase
from pages.usecases.review.delete_review import DeleteReviewUseCase
from pages.usecases.review.get_review_by_book import GetReviewsByBookUseCase
from pages.usecases.review.get_review_by_user import GetReviewsByUserUseCase


def create_test_review(user_id=None, book_id=None) -> Review:
    return Review(
        id=str(uuid.uuid4()),
        book_id=book_id or str(uuid.uuid4()),
        user_id=user_id or str(uuid.uuid4()),
        review="Comentário de teste",
        date="2025-06-09",
    )


@pytest.mark.asyncio
async def test_add_review():
    repo = InMemoryReviewRepository()
    review = create_test_review()
    usecase = AddReviewUseCase(repo)

    result = await usecase.execute(review)

    assert result == review
    assert repo._reviews[review.id] == review


@pytest.mark.asyncio
async def test_get_reviews_by_book():
    repo = InMemoryReviewRepository()
    book_id = str(uuid.uuid4())
    review1 = create_test_review(book_id=book_id)
    review2 = create_test_review(book_id=book_id)
    review_other = create_test_review()

    await repo.add_review(review1)
    await repo.add_review(review2)
    await repo.add_review(review_other)

    usecase = GetReviewsByBookUseCase(repo)
    result = await usecase.execute(book_id)

    assert review1 in result
    assert review2 in result
    assert review_other not in result
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_reviews_by_book_empty():
    repo = InMemoryReviewRepository()
    usecase = GetReviewsByBookUseCase(repo)
    result = await usecase.execute("book-vazio")

    assert result == []


@pytest.mark.asyncio
async def test_get_reviews_by_user():
    repo = InMemoryReviewRepository()
    user_id = str(uuid.uuid4())
    review1 = create_test_review(user_id=user_id)
    review2 = create_test_review(user_id=user_id)
    review_other = create_test_review()

    await repo.add_review(review1)
    await repo.add_review(review2)
    await repo.add_review(review_other)

    usecase = GetReviewsByUserUseCase(repo)
    result = await usecase.execute(user_id)

    assert review1 in result
    assert review2 in result
    assert review_other not in result
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_reviews_by_user_empty():
    repo = InMemoryReviewRepository()
    usecase = GetReviewsByUserUseCase(repo)
    result = await usecase.execute("user-vazio")

    assert result == []


@pytest.mark.asyncio
async def test_delete_review():
    repo = InMemoryReviewRepository()
    review = create_test_review()
    await repo.add_review(review)

    usecase = DeleteReviewUseCase(repo)
    await usecase.execute(review.id)

    assert review.id not in repo._reviews


@pytest.mark.asyncio
async def test_delete_review_not_found():
    repo = InMemoryReviewRepository()
    usecase = DeleteReviewUseCase(repo)

    # Só garante que não levanta erro
    await usecase.execute("id-invalido")
