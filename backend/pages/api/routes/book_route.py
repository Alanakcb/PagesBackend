from fastapi import APIRouter, HTTPException, Depends
from pages.usecases.book.create_book import CreateBookUseCase
from pages.usecases.book.delete_book import DeleteBookUseCase
from pages.usecases.book.get_all_books import GetAllBooksUseCase
from pages.usecases.book.get_book_by_id import GetBookByIdUseCase
from pages.usecases.book.update_book import UpdateBookUseCase
from pages.domain.entities.book import Book
from pages.domain.entities.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from pages.api.deps import (
    get_user_repository,
    get_current_user,
    get_db_session,
    get_book_repository,
)
from typing import List
from pages.domain.repositories.book_repository import BookRepository

from pages.api.schemas.book_schema import BookCreateInput

import uuid
from pages.api.schemas.book_schema import BookOutput, BookCreateInput, BookUpdateInput
from pages.infra.repositories.sqlalchemy.sqlalchemy_book_repository import (
    SQLAlchemyBookRepository,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pages.api.schemas.book_schema import book_to_output, books_to_output

security = HTTPBearer()
router = APIRouter()


@router.get("/", response_model=List[BookOutput])
async def get_all_books(
    book_repo: BookRepository = Depends(get_book_repository),
):
    usecase = GetAllBooksUseCase(book_repo)
    books = await usecase.execute()
    return books_to_output(books)


@router.get("/{book_id}", response_model=BookOutput)
async def get_book_by_id(
    book_id: str,
    book_repo: BookRepository = Depends(get_book_repository),
):
    usecase = GetBookByIdUseCase(book_repo)
    book = await usecase.execute(book_id)
    print(f"Retrieved book: {book}")
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_to_output(book)


@router.post("/", response_model=BookOutput)
async def create_book(
    data: BookCreateInput,
    db: AsyncSession = Depends(get_db_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: User = Depends(get_current_user),
    book_repo: BookRepository = Depends(get_book_repository),
):
    usecase = CreateBookUseCase(book_repo)
    book = Book(
        id=str(uuid.uuid4()),
        title=data.title,
        description=data.description,
        content=data.content,
    )
    created_book = await usecase.execute(book)
    if not created_book:
        raise HTTPException(status_code=404, detail="Book not created")
    return book_to_output(created_book)


@router.put("/{book_id}", response_model=BookOutput)
async def update_book(
    book_id: str,
    data: BookUpdateInput,
    book_repo: BookRepository = Depends(get_book_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    usecase_get = GetBookByIdUseCase(book_repo)
    existing_book = await usecase_get.execute(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    updated_book = Book(
        id=book_id, title=data.title, description=data.description, content=data.content
    )
    usecase_update = UpdateBookUseCase(book_repo)
    result = await usecase_update.execute(updated_book)
    if not result:
        raise HTTPException(status_code=400, detail="Book not updated")
    return book_to_output(result)


@router.delete("/{book_id}")
async def delete_book(
    book_id: str,
    book_repo: BookRepository = Depends(get_book_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    usecase = DeleteBookUseCase(book_repo)
    success = await usecase.execute(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
