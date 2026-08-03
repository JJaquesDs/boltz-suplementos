from core.base_repository import Baserepository

from sqlmodel import Session, select

from models.users import Users


class UserRepository(Baserepository):
    """ Classe para repositório de usuários base """

    def __init__(self):

        super().__init__(
            model=Users,
            campo_id="user_id"
        )

    def get_by_email(self, session: Session, email: str) -> Users | None:
        """ Método para buscar usuário pelo email """

        return session.exec(
            statement=select(self.model).filter_by(email=email)).first()