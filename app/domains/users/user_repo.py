from sqlalchemy import func

from app.core.base_repository import Baserepository

from sqlmodel import Session, select

from app.domains import UserRole
from app.domains.users.users import Users


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

    def count_superusers(self, session: Session) -> int:
        """Método para contar quantos superusuários existem"""
        statement = select(func.count(self.model.user_id)).where(
            self.model.role == UserRole.SUPERUSER
        )
        result = session.exec(statement).first()
        return result if result else 0
