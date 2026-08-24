from fastapi import status, Depends
from sqlmodel import Session
from app.domains.users.users import Users
from app.core.database import get_session
from app.domains.users.enums.user_role import UserRole
from app.exceptions.exceptions import UnauthorizedError
from fastapi.security import OAuth2PasswordBearer

# ============================================================
# Esquema de autenticação
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/swagger")


def get_user_dep(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session)
) -> Users:
    """Método para pegar usuário autenticado"""

    from app.domains.users.services.user_service import UserService

    user_service = UserService()

    return user_service.get_current_user_service(session=session, token=token)


def exigir_roles_dep(roles: list[UserRole]):
    """Método para exigir um user role dentro dos roles existentes"""

    def checar_roles(user_atual: Users = Depends(get_user_dep)):
        """Método para checar roles específicos"""

        if user_atual.role not in roles:
            raise UnauthorizedError(
                message=f"Usuário não tem permissão necessária",
                codigo=status.HTTP_403_FORBIDDEN
            )
        return user_atual

    return checar_roles
