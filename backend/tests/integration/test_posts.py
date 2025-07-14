import pytest
from httpx import AsyncClient
import datetime


@pytest.mark.asyncio
async def test_create_and_get_books(client: AsyncClient):
    # Registro + login
    await client.book(
        "/users/register",
        json={
            "name": "Booker",
            "email": "booker@example.com",
            "password": "book@Test123",
            "role": "user",
        },
    )
    login_response = await client.book(
        "/users/login", json={"email": "booker@example.com", "password": "book@Test123"}
    )
    token = login_response.json()["access_token"]

    # Criação do book
    book_data = {
        "title": "Título de teste",
        "description": "Descrição curta",
        "content": "Conteúdo completo do book",
        "date": datetime.datetime.now().isoformat(),
    }

    response = await client.book(
        "/books/",
        json=book_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    book = response.json()
    assert book["title"] == book_data["title"]

    # GET /books
    response = await client.get("/books/")
    assert response.status_code == 200
    books = response.json()
    assert any(p["title"] == book_data["title"] for p in books)
