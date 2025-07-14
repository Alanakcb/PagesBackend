from datetime import datetime
from pages.domain.entities.user import User
from pages.domain.entities.review import Review
from typing import Optional, List


class Book:
    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        content: str,
        user_id: str,
        date: datetime,
        user: Optional[User] = None,
        reviews: Optional[List[Review]] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.content = content
        self.user_id = user_id
        self.date = date
        self.user = user
        self.reviews = reviews or []
