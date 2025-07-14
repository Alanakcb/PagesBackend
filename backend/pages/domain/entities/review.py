from datetime import datetime
from typing import Optional, List
from pages.domain.entities.user import User


class Review:
    def __init__(
        self,
        id: str,
        book_id: str,
        user_id: str,
        review: str,
        date: datetime,
        user: Optional[User] = None,
    ):
        self.id = id
        self.book_id = book_id
        self.user_id = user_id
        self.review = review
        self.date = date
        self.user = user
