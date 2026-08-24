from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from uuid import UUID

from app.domains.users.users import Users
from app.domains.users.services.user_service import UserService
from app.domains.users.services.auth_service import AuthService
from app.domains.users.schemas.auth_schemas import Token, LoginRequest
from app.core.dependencies import get_user_dep, get_session
from app.domains.users.schemas.users_schemas import UserPublic, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()


@router.post(
    path="/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo usuário"
)
def create_user(
        user_data: UserCreate,
        session: Session = Depends(get_session)
):
    return user_service.create_user_service(
        session=session,
        obj_request=user_data,
        user_atual=None
    )


@router.get(
    path="/listar_todos",
    response_model=list[UserPublic],
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de usuários"
)
def list_all(
        session: Session = Depends(get_session),
        user_atual: Users = Depends(get_user_dep)
):
    """Retorna todos os registros de usuários"""
    return user_service.get_all_service(session=session)


@router.get(
    path="/{user_id}",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
    summary="Retorna um usuário pelo UUID"
)
def list_user_by_id(
        user_id: UUID,
        session: Session = Depends(get_session),
        user_atual: Users = Depends(get_user_dep)
):
    """Retorna um usuário pelo user_id(UUID)"""
    return user_service.get_user_by_id_service(
        session=session,
        user_id=user_id
    )


@router.patch(
    path="/{user_id}",
    response_model=UserPublic,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Atualiza um usuário existente pelo UUID"
)
def update_user(
        user_id: UUID,
        user_update: UserUpdate,
        session: Session = Depends(get_session),
        user_atual: Users = Depends(get_user_dep)
):
    """Atualiza um usuário pelo user_id(UUID)"""
    return user_service.update_user_service(
        session=session,
        model_id=user_id,
        obj_request=user_update,
        user_atual=user_atual
    )


# ============================================================
# ENDPOINTS DE LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login com JSON (para frontend/Postman)"
)
def login_json(
        credentials: LoginRequest,
        session: Session = Depends(get_session)
):
    """
    Login de usuário com JSON
    """
    auth_service = AuthService()

    # Autentica o usuário
    user = auth_service.authenticate(
        session=session,
        email=credentials.email,
        password=credentials.password
    )

    # Cria o token
    access_token = auth_service.create_access_token(user_id=user.user_id)

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.post(
    "/login/swagger",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login com OAuth2 (para Swagger UI)"
)
def login_oauth2(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    """
    Login de usuário com OAuth2 (form-data)
    """
    auth_service = AuthService()

    # OAuth2 usa 'username' como campo
    user = auth_service.authenticate(
        session=session,
        email=form_data.username,
        password=form_data.password
    )

    access_token = auth_service.create_access_token(user_id=user.user_id)

    return Token(
        access_token=access_token,
        token_type="bearer"
    )
