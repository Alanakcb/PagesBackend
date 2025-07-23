from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from datetime import datetime
from pages.api.schemas.user_schema import UserOutput
from pages.domain.entities.book import Book
from pages.api.schemas.user_schema import user_to_output


class BookCreateInput(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Título do book")
    description: str = Field(
        ..., min_length=10, max_length=300, description="Descrição do book"
    )
    content: str = Field(..., min_length=20, description="Conteúdo do book")


class BookUpdateInput(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Título do book")
    description: str = Field(
        ..., min_length=10, max_length=300, description="Descrição do book"
    )
    content: str = Field(..., min_length=20, description="Conteúdo do book")


class BookOutput(BaseModel):
    id: str = Field(..., description="ID do book")
    title: str = Field(..., min_length=3, max_length=100, description="Título do book")
    description: str = Field(
        ..., min_length=10, max_length=300, description="Descrição do book"
    )
    content: str = Field(..., min_length=20, description="Conteúdo do book")

    @classmethod
    def from_entity(cls, book):
        return cls(
            id=book.id,
            title=book.title,
            description=book.description,
            content=book.content,
        )


def book_to_output(book: Book) -> BookOutput:
    return BookOutput(
        id=book.id,
        title=book.title,
        content=book.content,
        description=book.description,
    )


def books_to_output(books: list[Book]) -> list[BookOutput]:
    return [book_to_output(book) for book in books]
