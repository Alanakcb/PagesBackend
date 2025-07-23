import pytest
from pages.domain.entities.user import User
from pages.domain.entities.book import Book
from pages.domain.entities.review import Review
from pages.domain.value_objects.email_vo import Email
from pages.domain.value_objects.password import Password


def test_create_user():
    email = Email("user@example.com")
    pwd = Password("Secret@123")
    user = User("1", "User", email, pwd, "user")
    assert user.name == "User"


def test_invalid_role():
    with pytest.raises(ValueError):
        User("1", "User", Email("user@example.com"), Password("Secret@123"), "invalid")


def test_create_book():
    book = Book("1", "Title", "Desc", "Content")
    assert book.title == "Title"


def test_create_review():
    review = Review("1", "book1", "user1", "Nice book!", "2024-01-01")
    assert review.review == "Nice book!"
