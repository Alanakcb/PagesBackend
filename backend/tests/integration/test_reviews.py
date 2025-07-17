import pytest
import datetime
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_get_reviews(client: AsyncClient):
    # 1. Registro do usuário
    await client.post(
        "/users/register",
        json={
            "name": "Comentador",
            "email": "review@example.com",
            "password": "test@Review123",
            "role": "user",
        },
    )

    # 2. Login
    login_response = await client.post(
        "/users/login",
        json={"email": "review@example.com", "password": "test@Review123"},
    )
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Criação de book para comentar
    book_response = await client.post(
        "/books/",
        json={
            "title": "Book para Comentário",
            "description": "Descrição do book",
            "content": "Conteúdo completo do book",
            "date": datetime.datetime.now().isoformat(),
        },
        headers=headers,
    )
    assert book_response.status_code == 200
    book_id = book_response.json()["id"]

    # 4. Criar comentário
    review_response = await client.post(
        "/reviews/",
        json={
            "book_id": book_id,
            "review": "Primeiro comentário!",
            "date": datetime.datetime.now().isoformat(),
        },
        headers=headers,
    )
    assert review_response.status_code == 200
    review_data = review_response.json()
    assert review_data["review"] == "Primeiro comentário!"
    assert review_data["book_id"] == book_id

    # 5. Buscar comentários por book
    list_response = await client.get(f"/reviews/book/{book_id}", headers=headers)
    assert list_response.status_code == 200
    reviews = list_response.json()
    assert any(c["review"] == "Primeiro comentário!" for c in reviews)
