from fastapi import FastAPI
from app.api.main import api_router
from sqlmodel import SQLModel, Session
from contextlib import asynccontextmanager
from app.core.database import engine, init_db
from app.exceptions.exceptions import AppException
from app.api.exceptions_handlers import app_exception_handler

from app.api.exceptions_handlers import (
    RequestValidationError,
    validation_exception_handler,
    IntegrityError,
    database_exception_handler,
    generic_exception_handler
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Função assíncrona para inicializar db ao subir aplicação"""

    try:
        SQLModel.metadata.create_all(engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f" Erro ao iniciar tabelas{e}")
        raise

    try:
        with Session(engine) as session:
            init_db(session)
    except Exception as e:
        print(f"Erro ao inicializar SUPERUSER: {e}")
        raise

    yield

app = FastAPI(
    title="Boltz Suplementos API",
    lifespan=lifespan
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, database_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(api_router)
