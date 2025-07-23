from fastapi import FastAPI
from fastapi.security import HTTPBearer
from pages.api.routes import review_route, book_route, user_route
from pages.api.openapi_tags import openapi_tags
from fastapi.middleware.cors import CORSMiddleware
import uuid
from pages.infra.models.book_model import BookModel
from pages.infra.database import async_session, engine
from pages.api.mock_posts import mock_posts
import sqlalchemy as sa
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Database tables created/checked on startup.")

    async with async_session() as db:
        try:
            # Verifica se a tabela "books" já contém registros
            total_books_result = await db.execute(
                sa.select(sa.func.count()).select_from(BookModel)
            )
            qtd_books = total_books_result.scalar_one()

            if qtd_books == 0:
                print("Banco de livros vazio. Populando com dados iniciais...")

                for book_data in mock_posts:
                    await db.execute(
                        sa.text(
                            """
                            INSERT INTO books (id, title, description, content)
                            VALUES (:id, :title, :description, :content)
                        """
                        ),
                        {
                            "id": str(uuid.uuid4()),
                            "title": book_data["title"],
                            "description": f"Obra escrita por {book_data['autor']}.",
                            "content": f"{book_data['figure']}",
                        },
                    )

                await db.commit()
                print("Livros adicionados com sucesso.")
            else:
                print(
                    f"Banco já contém {qtd_books} livros. Nenhuma população necessária."
                )

        except Exception as e:
            print(f"Erro ao inserir livros: {e}")
            await db.rollback()
        finally:
            pass

    yield
    await engine.dispose()
    print("Database engine disposed on shutdown.")


app = FastAPI(
    title="Pages API",
    description="API backend do Pages com Clean Architecture, FastAPI e PostgreSQL",
    version="1.0.0",
    contact={"name": "Alana e Luana", "email": "alanaluana@gmail.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    openapi_tags=openapi_tags,
    redirect_slashes=True,
    lifespan=lifespan,
)

origins = [
    "http://localhost:5173",  # Vite local
    "https://frontclean.vercel.app",  # Produção
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # lista de origens confiáveis
    allow_credentials=True,
    allow_methods=["*"],  # ou especifique ["GET", "POST"]
    allow_headers=["*"],
)


@app.get("/")
def ola():
    return {"olá": "fastapi"}


app.include_router(user_route.router, prefix="/users", tags=["Users"])
app.include_router(book_route.router, prefix="/books", tags=["Books"])
app.include_router(review_route.router, prefix="/reviews", tags=["Reviews"])
