from uuid import UUID
from sqlmodel import Session
from fastapi import status
import logging

from app.core.security import JWTManipulador
from app.domains.users.users import Users
from app.domains.users.user_repo import UserRepository
from app.domains.users.services.password_service import PasswordService
from app.exceptions.exceptions import InvalidCredentialsError, EntityNotFoundError

logger = logging.getLogger(__name__)


class AuthService:
    """Gerencia autenticação e autorização de usuários"""

    def __init__(
            self,
            user_repository: UserRepository | None = None,
            password_service: PasswordService | None = None
    ):
        self.user_repository = user_repository or UserRepository()
        self.password_service = password_service or PasswordService()
        self.jwt_handler = JWTManipulador()

    def authenticate(
            self,
            session: Session,
            email: str,
            password: str
    ) -> Users:
        """Método para autenticar um usuário por email e senha"""

        user = self.user_repository.get_by_email(session=session, email=email)

        if not user:
            logger.warning(f"Tentativa de login com email inexistente: {email}")
            raise InvalidCredentialsError(
                message="Email ou senha incorretos",
                codigo=status.HTTP_401_UNAUTHORIZED
            )

        if not self.password_service.verify_password(
            senha_simples=password,
            hashed_password=user.senha
        ):
            logger.warning(f"Senha incorreta para o email: {email}")
            raise InvalidCredentialsError(
                message="Email ou senha incorretos",
                codigo=status.HTTP_401_UNAUTHORIZED
            )

        logger.info(f"Login bem-sucedido: {email}")
        return user

    def create_access_token(self, user_id: UUID) -> str:
        """Método para apenas retornar o token de acesso"""
        return self.jwt_handler.create_acess_token(user_id=user_id)

    def get_user_from_token(
            self,
            session: Session,
            token: str
    ) -> Users:
        """Método para validar um token de usuário válido"""

        try:
            payload = self.jwt_handler.decode_token(token)
            user_id_str: str | None = payload.get("sub")

            if not user_id_str:
                raise InvalidCredentialsError(
                    message="Token inválido",
                    codigo=status.HTTP_401_UNAUTHORIZED
                )

            user_id = UUID(user_id_str)

        except Exception as e:
            logger.error(f"Erro ao decodificar token: {str(e)}")
            raise InvalidCredentialsError(
                message="Token inválido ou expirado",
                codigo=status.HTTP_401_UNAUTHORIZED
            )

        user = self.user_repository.get_by_id(session=session, model_id=user_id)

        if not user:
            raise EntityNotFoundError(
                message="Usuário não encontrado",
                codigo=status.HTTP_404_NOT_FOUND
            )

        return user