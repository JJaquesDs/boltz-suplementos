from uuid import UUID

from sqlmodel import Session

from repository.user_repo import UserRepository

from core.base_service import BaseService, CreateTipoSchema

from models.users import Users
from schemas.users_schemas import (
    UserPublic,
    UserCreate,
    UserUpdate,
    UserReadSenha
)


class UserService(BaseService[
                      Users,
                      UserPublic,
                      UserCreate,
                      UserUpdate,
                      UserReadSenha
]):
    """ Classe para usar serviços de negócios de Usuários """

    def __init__(self):
        """ Inicialização da classe """

        super().__init__(repository=UserRepository())

    def _validade_crate_service(self, session: Session, obj_request: CreateTipoSchema):
        """ Validação de criação de um usuário todo:(adicionar mais validações, criação superuser e admins) """

        if self.repository.get_by_email(session=session, email=obj_request.email):
            raise ValueError(f"Email {obj_request.email} já existe nos registros")

    def _validate_delete_service(
            self,
            model_id: UUID,
            session: Session
    ) -> None:
        """ Validação de deleção de um usuário todo:adicionar validação deleção superusers e admins"""

        result = self.repository.get_by_id(session=session, model_id=model_id)

        if not result:
            raise ValueError(f"Usuário não encontrado com ID: {model_id}")

    def _authenticate_user_service(self):
        pass

    def _get_password_hash_user_service(self):
        pass
