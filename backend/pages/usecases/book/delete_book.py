from pages.domain.repositories.book_repository import BookRepository


class DeleteBookUseCase:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def execute(self, book_id: str) -> bool:
        await self.repository.delete(book_id)
        return True
