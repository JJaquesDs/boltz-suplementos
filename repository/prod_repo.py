from core.base_repository import Baserepository

from sqlmodel import Session, select

from models.produtos import Produto


class ProdutosRepository(Baserepository):
    """ Classe para repositório de usuários """

    def __init__(self):

        super().__init__(
            model=Produto,
            campo_id="prod_id"
        )

    def get_by_codigo(
            self,
            session: Session,
            cod_prod: str
    ) -> Produto | None:
        """ Método para retornar um produto pelo código"""

        return session.exec(
            statement=select(self.model).filter_by(cod_prod=cod_prod)
        ).first()

