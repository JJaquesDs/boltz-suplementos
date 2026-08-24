import jwt

from uuid import UUID

from sqlmodel import Session

from typing import Optional, List

from app.core.config import settings

from fastapi import HTTPException, status

from app.core.database import get_session
from app.domains.users.users import Users

from app.domains.users.enums.user_role import UserRole

from app.domains.users.user_repo import UserRepository

from app.domains.users.services.password_service import PasswordService

from app.exceptions.exceptions import UnauthorizedError, EntityNotFoundError

from app.core.base_service import (
    BaseService,
    CreateTipoSchema,
    TipoModel
)

from app.domains.users.schemas.users_schemas import (
    UserPublic,
    UserCreate,
    UserUpdate
)


class UserService(BaseService[
                      Users,
                      UserPublic,
                      UserCreate,
                      UserUpdate,
                      UserRepository
]):
    """ Classe para usar serviços de negócios de Usuários """

    def __init__(
            self,
            repository: UserRepository | None = None,
            password_service: PasswordService | None = None
    ):
        """ Inicialização da classe """

        super().__init__(repository=repository or UserRepository())
        self.password_service = password_service or PasswordService()

    def _validade_create_service(
            self, session: Session,
            obj_request: CreateTipoSchema,
            **kwargs
    ):
        """ Validação de criação de permissoes de um usuário """

        # Opicional, pois pode tentar cadastrar novo usuário normal
        user_atual: Optional[Users] = kwargs.get("user_atual")

        # Inicialização do banco, user_atual vazio, e role superuser
        # (porém só aceita caso não houver registro de outro superuser no banco
        if user_atual is None and obj_request.role == UserRole.SUPERUSER:
            total_superusers = self.repository.count_superusers(session)

            if total_superusers == 0:
                return  # Permite criar sem mais validações
            else:
                raise UnauthorizedError(
                    message="Já existe superusuário. Apenas superusuários podem criar novos.",
                    codigo=status.HTTP_401_UNAUTHORIZED
                )

        # Validação de email único
        if self.repository.get_by_email(
                session=session,
                email=obj_request.email
        ):
            raise ValueError(f"Email {obj_request.email} já existe nos registros")

        # Se user_atual não estiver autenticado e quiser criar usuário diferente do normal não autoriza
        if user_atual is None:
            if obj_request.role != UserRole.USER:
                raise UnauthorizedError(
                    message="Sem permissão para criar outro tipo de usuário",
                    codigo=status.HTTP_401_UNAUTHORIZED
                )

        # Se tiver autenticado, valida o role
        else:
            self._validate_role_service(
                user_atual=user_atual,
                role_alvo=obj_request.role
            )

    def _validate_delete_user_service(
            self,
            model_id: UUID,
            session: Session,
            user_atual: Users
    ) -> None:
        """ Validação de deleção de um usuário """

        result = self.repository.get_by_id(
            session=session,
            model_id=model_id
        )

        if not result:
            raise EntityNotFoundError(
                message=f"Usuário não encontrado com ID: {model_id}",
                codigo=status.HTTP_404_NOT_FOUND
            )

        # Validação de role para não deletar superusuários ou administradores
        self._validate_role_service(
            user_atual=user_atual,
            role_alvo=user_atual.role
        )

    @staticmethod
    def _validate_role_service(
            role_alvo: UserRole,
            user_atual: Optional[Users]
    ):
        """ Serviço para validação de permissões de roles """

        # Se o user_atual não estiver autenticado e tentar manipular outros não permite
        if user_atual is None:
            if role_alvo in [UserRole.SUPERUSER, UserRole.ADMIN]:
                raise UnauthorizedError(
                    message="Apenas superusuários podem manipular usuários administradores",
                    codigo=status.HTTP_401_UNAUTHORIZED
                )

            # User pode ser criado sem autenticação (cadastro)
            return

        if (
                role_alvo in
                [UserRole.SUPERUSER, UserRole.ADMIN] and
                user_atual.role != UserRole.SUPERUSER
        ):
            raise UnauthorizedError(
                message="Apenas superusuários podem manipular usuários administradores",
                codigo=status.HTTP_401_UNAUTHORIZED
            )

    @staticmethod
    def _validate_update_service(
            user_alvo: Users,
            user_atual: Users
    ):
        """ Service para validar atualizações em usuários """

        # Regra de não alteração de superusers
        if user_alvo.role == UserRole.SUPERUSER:
            raise UnauthorizedError(
                message="Superusuários não podem ser modificados",
                codigo=status.HTTP_401_UNAUTHORIZED
            )

        # Regra de não alteração de admins por usuários comuns(nem outros admins)
        if (
                user_alvo.role == UserRole.ADMIN and
                user_atual.role != UserRole.SUPERUSER
        ):
            raise UnauthorizedError(
                message="Somente superusuários podem alterar administradores ",
                codigo=status.HTTP_401_UNAUTHORIZED
            )

        # Regra de não alteração de usuários por outros usuários comuns
        if user_atual.role == UserRole.USER:
            raise UnauthorizedError("Usuários não podem modificar outros usuários")

    def get_current_user_service(self, session: Session, token: str) -> Users:
        """ Service que valida token e retorna Usuario """

        exception_credenciais = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"}
        )

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            user_id: UUID | None = payload.get("sub")

            if user_id is None:
                raise exception_credenciais

        except jwt.PyJWTError:
            raise exception_credenciais

        user = self.get_by_id_service(session=session, model_id=user_id)

        if not user:
            raise EntityNotFoundError(
                message="Usuário não encontrado",
                codigo=status.HTTP_404_NOT_FOUND,
            )

        return user

    def create_user_service(
            self,
            session: Session,
            obj_request: UserCreate,
            user_atual: Users | None
    ) -> Users:

        senha_hash = self.password_service.hash_password(
            password=obj_request.senha
        )

        user = Users(
            nome=obj_request.nome,
            email=obj_request.email,
            senha=senha_hash,
            role=UserRole.USER
        )

        self._validade_create_service(session=session, obj_request=user, user_atual=user_atual)

        return self.repository.create(
            session=session,
            obj_request=user
        )

    def get_user_by_id_service(
            self,
            session: Session,
            user_id: UUID
    ) -> Optional[UserPublic]:
        """
        Método para retornar um usuário

        Modificado para retornar um usuário público
        """

        user = super().get_by_id_service(session=session, model_id=user_id)

        return UserPublic.model_validate(user)

    def get_all_service(self, session: get_session) -> List[UserPublic]:

        users = self.repository.get_all(session=session)

        return [UserPublic.model_validate(user) for user in users]

    def update_user_service(
            self,
            session: Session,
            model_id: UUID,
            obj_request: UserUpdate,
            user_atual: Users
    ) -> TipoModel:
        """
        Método para atualizar um usuário

        Modificado para usar permissões de atualização
        """

        # Buscando se usuário existe
        user_alvo = self.get_by_id_service(
            session=session,
            model_id=model_id
        )

        self._validate_update_service(
            user_alvo=user_alvo,
            user_atual=user_atual
        )

        # Se estiver tentando mudar a senha, faz o hash
        if obj_request.senha:
            obj_request.senha = self.password_service.hash_password(
                password=obj_request.senha
            )

        user_update = self.update_service(
            session=session,
            model_id=model_id,
            obj_request=obj_request
        )

        return user_update
