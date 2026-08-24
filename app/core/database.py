from app.core.config import settings

from app.domains.users.enums.user_role import UserRole

from app.domains.users.schemas.users_schemas import UserCreate

from sqlmodel import create_engine, Session, select

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_session():
    """ Função para criar engine de sessões com o banco de dados """
    with Session(engine) as session:
        yield session


def init_db(session: Session) -> None:
    """ Inicializaa dados inicias com primeiro 'Superusuário' caso não houver """

    from app.domains.users.users import Users
    from app.domains.users.services.user_service import UserService

    user_service = UserService()

    superuser = session.exec(
        statement=select(Users).filter_by(email=settings.FIRST_SUPERUSER)
    ).first()

    if not superuser:
        user_service.create_user_service(
            session=session,
            obj_request=UserCreate(
                nome="SUPERUSUÁRIO",
                email=settings.FIRST_SUPERUSER,
                senha=settings.FIRST_SUPERUSER_PASSWORD,
                role=UserRole.SUPERUSER
            ),
            user_atual=None
        )

    session.commit()
