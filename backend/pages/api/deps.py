# Instâncias SQLAlchemy
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pages.api.settings import settings
from pages.domain.repositories.user_repository import UserRepository
from pages.infra.repositories.sqlalchemy.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from pages.infra.repositories.sqlalchemy.sqlalchemy_book_repository import (
    SQLAlchemyBookRepository,
)
from pages.infra.repositories.sqlalchemy.sqlalchemy_review_repository import (
    SQLAlchemyReviewRepository,
)
from sqlalchemy.ext.asyncio import AsyncSession
from pages.infra.database import async_session
from pages.domain.entities.user import User
from collections.abc import AsyncGenerator


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_user_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)


async def get_book_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyBookRepository:
    return SQLAlchemyBookRepository(db)


async def get_review_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyReviewRepository:
    return SQLAlchemyReviewRepository(db)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = str(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
        user = await user_repo.get_by_id(user_id)
        if user is None:
            raise credentials_exception
        await user_repo.set_current_user(user)
    except JWTError:
        raise credentials_exception

    user = await user_repo.get_current_user()
    if user is None:
        raise credentials_exception
    return user
