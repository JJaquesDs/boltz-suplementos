# app/api/exceptions_handlers.py

import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from app.exceptions.exceptions import AppException

logger = logging.getLogger(__name__)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handler para exceções customizadas da aplicação.

    Converte exceções de negócio em respostas HTTP padronizadas.
    """

    # Log do erro
    logger.warning(
        f"AppException: {exc.codigo} - {exc.message}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "status_code": exc.status_code
        }
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    Handler para erros de validação do Pydantic.

    Formata erros de validação de forma amigável.
    """

    logger.warning(
        f"Validation error: {exc.errors()}",
        extra={"path": request.url.path}
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Dados inválidos",
            "details": exc.errors()
        }
    )


async def database_exception_handler(
    request: Request,
    exc: IntegrityError
) -> JSONResponse:
    """
    Handler para erros de integridade do banco de dados.

    Evita vazar detalhes do banco para o cliente.
    """

    logger.error(
        f"Database error: {str(exc)}",
        extra={"path": request.url.path},
        exc_info=True
    )

    # Não vaza detalhes do banco
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "DATABASE_ERROR",
            "message": "Erro ao processar operação no banco de dados"
        }
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """
    Handler genérico para exceções não tratadas.

    Última linha de defesa - registra o erro e retorna resposta genérica.
    """

    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "path": request.url.path,
            "method": request.method
        },
        exc_info=True
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_ERROR",
            "message": "Erro interno do servidor"
        }
    )