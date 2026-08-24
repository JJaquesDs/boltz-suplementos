from uuid import UUID

from app.core.base_repository import Baserepository

from app.core.dependencies import get_session

from typing import TypeVar, Generic, Optional, List

from app.exceptions.exceptions import EntityNotFoundError


TipoModel = TypeVar("TipoModel")
PublicTipoSchema = TypeVar("PublicTipoSchema")
CreateTipoSchema = TypeVar("CreateTipoSchema")
UpdateTipoSchema = TypeVar("UpdateTipoSchema")

TipoRepository = TypeVar("TipoRepository", bound=Baserepository)


class BaseService(Generic[
    TipoModel,
    PublicTipoSchema,
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
            session: get_session,
            model_id: UUID
    ) -> Optional[TipoModel]:
        """ Método para retornar uma entidade pelo id (Pode retornar vazio)

            ATENÇÂO (Converta a entidade para schemas nas classes services filhas, para não retornar senhas, por exemplo)
        """

        entity = self.repository.get_by_id(session=session, model_id=model_id)

        if not entity:
            raise EntityNotFoundError(f"Entidade {model_id} não encontrada")
        return entity

    def get_all_service(self, session: get_session) -> List[TipoModel]:
        """ Método para retornar todas as entidades """

        return self.repository.get_all(session=session)

    def _validate_delete_service(
            self,
            model_id: UUID,
            session: get_session
    ) -> None:
        """ Hook para validações antes de deletar entidades (Sobreescre para validações específicas) """

        pass

    def _validade_create_service(
            self,
            session: get_session,
            obj_request: CreateTipoSchema,
            **kwargs
    ):
        """ Hook para validação de criação de entidades (Sobreescreva para validação específica da entidade) """

        pass

    def create_service(
            self,
            session: get_session,
            obj_request: CreateTipoSchema,
            **kwargs
    ) -> TipoModel:
        """ Método para instânciar novas entidades (sobreescreva para adicionar validações) """

        self._validade_create_service(session=session, obj_request=obj_request, **kwargs)

        self.repository.create(session=session, obj_request=CreateTipoSchema())

        return obj_request

    def update_service(
            self,
            session: get_session,
            model_id: UUID,
            obj_request: UpdateTipoSchema
    ) -> TipoModel:
        """ Método para atualizar entidades """

        db_registro = self.get_by_id_service(
            session=session,
            model_id=model_id
        )

        obj_update = self.repository.update(
            session=session,
            obj_db=db_registro,
            obj_request=obj_request
        )

        return obj_update

    def delete_service(self, session: get_session, model_id: UUID):
        """ Método para deletar entidades """

        self._validate_delete_service(
            session=session,
            model_id=model_id
        )

        result = self.repository.delete(
            session=session,
            model_id=model_id
        )

        return result

