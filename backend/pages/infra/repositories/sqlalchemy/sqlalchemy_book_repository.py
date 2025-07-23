from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from pages.domain.entities.book import Book
from pages.domain.repositories.book_repository import BookRepository
from pages.infra.models.book_model import BookModel
from sqlalchemy.orm import joinedload


class SQLAlchemyBookRepository(BookRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> List[Book]:
        result = await self._session.execute(select(BookModel))
        books = result.unique().scalars().all()
        print(books)
        return [book.to_entity() for book in books]

    async def get_by_id(self, book_id: str) -> Optional[Book]:
        result = await self._session.execute(
            select(BookModel).where(BookModel.id == book_id)
        )
        book = result.unique().scalar_one_or_none()
        return book.to_entity() if book else None

    async def create(self, book: Book) -> Book:
        db_book = BookModel.from_entity(book)
        self._session.add(db_book)
        await self._session.commit()
        await self._session.refresh(db_book)
        return db_book.to_entity()

    async def update(self, book: Book) -> Optional[Book]:
        stmt = (
            update(BookModel)
            .where(BookModel.id == book.id)
            .values(
                title=book.title,
                description=book.description,
                content=book.content,
                user_id=book.user_id,
                date=book.date,
            )
            .returning(BookModel)
        )
        await self._session.execute(stmt)
        await self._session.commit()
        result = await self._session.execute(
            select(BookModel)
            .options(joinedload(BookModel.user), joinedload(BookModel.reviews))
            .where(BookModel.id == book.id)
        )
        updated = result.unique().scalar_one_or_none()
        return updated.to_entity() if updated else None

    async def delete(self, book_id: str) -> None:
        await self._session.execute(delete(BookModel).where(BookModel.id == book_id))
        await self._session.commit()
