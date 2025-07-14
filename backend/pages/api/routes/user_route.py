from fastapi import APIRouter, HTTPException, Depends
from pages.usecases.user.register_user import RegisterUserUseCase
from pages.usecases.user.login_user import LoginUserUseCase
from pages.usecases.user.logout_user import LogoutUserUseCase
from pages.usecases.user.get_current_user import GetCurrentUserUseCase
from pages.domain.entities.user import User
from pages.domain.value_objects.email_vo import Email
from pages.domain.value_objects.password import Password, PasswordValidationError
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from pages.api.deps import get_db_session, get_user_repository, get_current_user
from pages.infra.repositories.sqlalchemy.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pages.api.schemas.user_schema import (
    RegisterUserInput,
    UserOutput,
    TokenResponse,
)
from pages.api.schemas.message_schema import MessageOutput
from pages.api.security import create_access_token
from pages.domain.repositories.user_repository import UserRepository
from pages.api.schemas.user_schema import LoginUserInput
from pages.api.security import verify_token

security = HTTPBearer()
router = APIRouter()

# ----------------------
# Register
# ----------------------


@router.post(
    "/register",
    response_model=MessageOutput,
    summary="Registrar novo usuário",
    description="Cria um novo usuário com nome, email e senha forte.",
)
async def register_user(
    data: RegisterUserInput, db: AsyncSession = Depends(get_db_session)
):
    try:
        user_repo = SQLAlchemyUserRepository(db)
        usecase = RegisterUserUseCase(user_repo)
        user = User(
            id=str(uuid.uuid4()),
            name=data.name,
            email=Email(data.email),
            password=Password(data.password),
            role=data.role,
        )
        await usecase.execute(user)
        return MessageOutput(
            message="User registered successfully"  # , user=UserOutput.from_entity(result)
        )
    except PasswordValidationError as p:
        raise HTTPException(status_code=400, detail=str(p))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------
# Login
# ----------------------


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Fazer o Login do usuário",
    description="Autentica um usuário com email e senha forte.",
)
async def login_user(
    data: LoginUserInput,
    user_repo: UserRepository = Depends(get_user_repository),
):
    try:
        usecase = LoginUserUseCase(user_repo)
        user = await usecase.execute(Email(data.email), Password(data.password))
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token(data={"sub": user.id})
        return TokenResponse(
            access_token=token, token_type="bearer", user=UserOutput.from_entity(user)
        )
    except PasswordValidationError as p:
        raise HTTPException(status_code=400, detail=str(p))
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


# ----------------------
# Get Current User
# ----------------------


@router.get(
    "/me",
    response_model=UserOutput,
    summary="Informar os dados do usuário atual",
    description="Retorna os dados do usuário atual.",
)
async def get_me_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: User = Depends(get_current_user),
):
    try:
        return {
            "id": user.id,
            "name": user.name,
            "email": str(user.email),
            "role": user.role,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
