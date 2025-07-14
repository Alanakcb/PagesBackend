import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from pages.domain.entities.review import Review
import uuid
from datetime import datetime
from pages.infra.database import Base


class ReviewModel(Base):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(
        sa.String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    review: Mapped[str] = mapped_column(sa.Text, nullable=False)
    book_id: Mapped[str] = mapped_column(
        sa.String, sa.ForeignKey("books.id", ondelete="CASCADE")
    )
    user_id: Mapped[str] = mapped_column(
        sa.String, sa.ForeignKey("users.id", ondelete="CASCADE")
    )
    date: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.now())

    book = relationship("BookModel", back_populates="reviews", lazy="joined")
    user = relationship("UserModel", back_populates="reviews", lazy="joined")

    @classmethod
    def from_entity(cls, entity: Review) -> "ReviewModel":
        return cls(
            id=entity.id,
            review=entity.review,
            book_id=entity.book_id,
            user_id=entity.user_id,
            date=entity.date,
        )

    def to_entity(self) -> Review:
        return Review(
            id=self.id,
            review=self.review,
            book_id=self.book_id,
            user_id=self.user_id,
            date=self.date,
            user=self.user.to_entity(),
        )
