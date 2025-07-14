import uuid
import pytest
from pages.domain.entities.book import Book
from pages.infra.repositories.in_memory.in_memory_book_repository import (
    InMemoryBookRepository,
)
from pages.usecases.book.create_book import CreateBookUseCase
from pages.usecases.book.delete_book import DeleteBookUseCase
from pages.usecases.book.get_all_books import GetAllBooksUseCase
from pages.usecases.book.get_book_by_id import GetBookByIdUseCase
from pages.usecases.book.update_book import UpdateBookUseCase


def create_test_book() -> Book:
    return Book(
        id=str(uuid.uuid4()),
        title="Título de Exemplo",
        description="Descrição de Exemplo",
        content="Conteúdo do book",
        user_id=str(uuid.uuid4()),
        date="2025-06-09",
    )


@pytest.mark.asyncio
async def test_create_book():
    repo = InMemoryBookRepository()
    usecase = CreateBookUseCase(repo)
    book = create_test_book()

    result = await usecase.execute(book)

    assert result == book
    assert await repo.get_by_id(book.id) == book


@pytest.mark.asyncio
async def test_get_all_books():
    repo = InMemoryBookRepository()
    book1 = create_test_book()
    book2 = create_test_book()
    await repo.create(book1)
    await repo.create(book2)

    usecase = GetAllBooksUseCase(repo)
    result = await usecase.execute()

    assert len(result) == 2
    assert book1 in result
    assert book2 in result


@pytest.mark.asyncio
async def test_get_book_by_id():
    repo = InMemoryBookRepository()
    book = create_test_book()
    await repo.create(book)

    usecase = GetBookByIdUseCase(repo)
    result = await usecase.execute(book.id)

    assert result == book


@pytest.mark.asyncio
async def test_get_book_by_id_not_found():
    repo = InMemoryBookRepository()
    usecase = GetBookByIdUseCase(repo)
    result = await usecase.execute("id-invalido")

    assert result is None


@pytest.mark.asyncio
async def test_update_book():
    repo = InMemoryBookRepository()
    book = create_test_book()
    await repo.create(book)

    updated = Book(
        id=book.id,
        title="Título Atualizado",
        description="Descrição Atualizada",
        content="Novo conteúdo",
        user_id=str(uuid.uuid4()),
        date="2025-06-10",
    )

    usecase = UpdateBookUseCase(repo)
    result = await usecase.execute(updated)

    assert result.title == "Título Atualizado"
    repo_book = await repo.get_by_id(book.id)
    assert repo_book.content == "Novo conteúdo"


@pytest.mark.asyncio
async def test_update_book_not_found():
    repo = InMemoryBookRepository()
    book = create_test_book()

    usecase = UpdateBookUseCase(repo)
    result = await usecase.execute(book)

    assert result is None


@pytest.mark.asyncio
async def test_delete_book():
    repo = InMemoryBookRepository()
    book = create_test_book()
    await repo.create(book)

    usecase = DeleteBookUseCase(repo)
    await usecase.execute(book.id)

    assert await repo.get_by_id(book.id) is None


@pytest.mark.asyncio
async def test_delete_book_not_found():
    repo = InMemoryBookRepository()
    usecase = DeleteBookUseCase(repo)

    # Apenas garantir que não levanta exceção
    await usecase.execute("id-invalido")
