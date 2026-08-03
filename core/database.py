from dotenv import load_dotenv

from sqlmodel import create_engine, Session

load_dotenv()


##TODO: fazer leitura do dotenv, fazer url de conexão

DATABASE_URL = (

)

engine = create_engine(DATABASE_URL, echo=True                       )


def engine():
    """ Função para criar engine de sessões com o banco de dados """
    with Session(engine) as session:
        yield session

