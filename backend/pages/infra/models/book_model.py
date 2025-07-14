import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from pages.domain.entities.book import Book
import uuid
from datetime import datetime
from pages.infra.database import Base


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[str] = mapped_column(
        sa.String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    description: Mapped[str] = mapped_column(sa.String, nullable=False)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    user_id: Mapped[str] = mapped_column(
        sa.String, sa.ForeignKey("users.id", ondelete="CASCADE")
    )
    date: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.now())

    user = relationship("UserModel", back_populates="books", lazy="joined")
    reviews = relationship(
        "ReviewModel",
        back_populates="book",
        lazy="joined",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @classmethod
    def from_entity(cls, entity: Book) -> "BookModel":
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            content=entity.content,
            user_id=entity.user_id,
            date=entity.date,
        )

    def to_entity(self) -> Book:
        return Book(
            id=self.id,
            title=self.title,
            description=self.description,
            content=self.content,
            user_id=self.user_id,
            date=self.date,
            user=self.user.to_entity(),
        )
