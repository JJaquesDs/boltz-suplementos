from uuid import UUID

from sqlmodel import Session

from typing import TypeVar, Generic, Optional, List

from base_repository import Baserepository


TipoModel = TypeVar("TipoModel")
CreateTipoSchema = TypeVar("CreateTipoSchema")
UpdateTipoSchema = TypeVar("UpdateTipoSchema")

TipoRepository = TypeVar("TipoRepository", bound=Baserepository)


class BaseService(Generic[
    TipoModel,
    CreateTipoSchema,
    UpdateTipoSchema,
    TipoRepository
]):
    """ Classe base para service e regras de negócios das demais entidades """

    def __init__(self, repository: TipoRepository):
        """ Inicialização da classe """

        self.repository = repository

    def get_by_id_service(
            self,
            session: Session,
            model_id: UUID
    ) -> Optional[TipoModel]:
        """ Método para retornar uma entidade pelo id (Pode retornar vazio) """

        entity = self.repository.get_by_id(session=session, model_id=model_id)

        if not entity:
            raise ValueError(f"Entidade com ID: {model_id} não encontradada")
        return entity

    def get_all_service(self, session: Session) -> List[TipoModel]:
        """ Método para retornar todas as entidades """

        return self.repository.get_all(session=session)

    def _validate_delete_service(
            self,
            model_id: UUID,
            session: Session
    ) -> None:
        """ Hook para validações antes de deletar entidades (Sobreescre para validações específicas) """

        pass

    def _validade_crate_service(
            self,
            session: Session,
            obj_request: CreateTipoSchema
    ):
        """ Hook para validação de criação de entidades (Sobreescreva para validação específica da entidade) """

        pass

    def create_service(
            self,
            session: Session,
            obj_request: CreateTipoSchema
    )-> TipoModel:
        """ Método para instânciar novas entidades (sobreescreva para adicionar validações) """

        self._validade_crate_service(obj_request=obj_request)

        self.repository.create(session=session, obj_request=obj_request)

        return obj_request

    def update_service(
            self,
            session: Session,
            model_id: UUID,
            obj_request: UpdateTipoSchema
    ) -> TipoModel:
        """ Método para atualizar entidades """

        db_registro = self.get_by_id_service(session=session, model_id=model_id)

        obj_update = self.repository.update(obj_db=db_registro, obj_request=obj_request)

        return obj_update

    def delete_service(self, session: Session, model_id: UUID):
        """ Método para deletar entidades """

        self._validate_delete_service(model_id=model_id)

        result = self.repository.delete(session=session, model_id=model_id)

        return result

