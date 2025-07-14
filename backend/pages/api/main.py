from fastapi import FastAPI
from fastapi.security import HTTPBearer
from pages.api.routes import review_route, book_route, user_route
from pages.api.openapi_tags import openapi_tags
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Pages API",
    description="API backend do Pages com Clean Architecture, FastAPI e PostgreSQL",
    version="1.0.0",
    contact={"name": "Alana e Luana", "email": "alanaluana@gmail.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    openapi_tags=openapi_tags,
    redirect_slashes=True,
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
