from uuid import UUID

from sqlmodel import Session, select

from typing import Type, TypeVar, Generic, List

TipoModel = TypeVar("TipoModel")
CreateTipoSchema = TypeVar("CreateTipoSchema")
UpdateTipoSchema = TypeVar("UpdateTipoSchema")


class Baserepository(Generic[TipoModel]):
    """ Classe de repositório base """

    def __init__(self, model: Type[TipoModel], campo_id: str):
        """ Inicialização da classe """

        self.model = model
        self.campo_id = campo_id

    def get_by_id(self, session: Session, model_id: UUID):
        """ Método para pegar registros pelo id """

        # retornando entidade baseada pela primary-key
        return session.get(entity=self.model, ident=model_id)

    def get_all(
            self,
            session: Session
    ) -> List[TipoModel]:
        """ Método para retornar todos os registros de uma entidade """

        statement = select(self.model)

        return list(session.exec(statement=statement).all())

    def create(
            self,
            session: Session,
            obj_request: CreateTipoSchema
    ) -> TipoModel:
        """ Método para instanciar um registro no banco de dados """

        # Conversão do objeto para um dicionário (json)
        dados = obj_request.model_dump()

        # Desempacontamento do dicionário em parâmetros nomeados (marcando o objeto para ser instânciado)
        obj_db = self.model(**dados)

        session.add(obj_db)
        session.commit()
        session.refresh(obj_db)

        return obj_db

    def update(
            self,
            session: Session,
            obj_db: TipoModel,
            obj_request: UpdateTipoSchema,
    ) -> TipoModel:
        """ Método para atualizar um registro no banco de dados """

        # Dados do obj request só recebem os campos que foram preenchidos
        dados = obj_request.model_dump(exclude_unset=True)

        """
        Percorre os dados de request:
            dados = {
                nome: "João"
            }
            
            field = nome, value = "João"
            
            setattr método atribui ao obj_db esses valores como: obj_db.nome = "João"
        """
        for field, value in dados.items():
            setattr(obj_db, field, value)

        session.add(obj_db)
        session.commit()
        session.refresh(obj_db)

        return obj_db

    def delete(
            self, session: Session, model_id: UUID
    ) -> bool:
        """ Método para deletar um registro do banco de dados """

        # utilizando método get_by_id para encontrar o registro
        obj_db = self.get_by_id(session=session, model_id=model_id)

        # se encontrar deleta, caso não encontre retorna falso
        if obj_db:
            session.delete(obj_db)
            session.commit()
            return True
        return False

