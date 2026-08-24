# app/exceptions/exceptions.py

from typing import Any

from fastapi import status


class AppException(Exception):
    """
    Exceção base da aplicação.

    Todas as exceções customizadas devem herdar desta classe.
    Define um contrato para exceções de negócio.
    """

    status_code: int = status.HTTP_400_BAD_REQUEST
    default_message: str = "Erro na aplicação"

    def __init__(
            self,
            message: str | None = None,
            codigo: str | None = None,
            details: dict[str, Any] | None = None
    ):
        """
        Args:
            message: Mensagem de erro customizada
            codigo: Código de erro para o cliente (ex: "USER_NOT_FOUND")
            details: Detalhes adicionais estruturados
        """
        self.message = message or self.default_message
        self.codigo = codigo or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Serializa a exceção para resposta JSON"""
        response = {
            "error": self.codigo,
            "message": self.message,
        }
        if self.details:
            response["details"] = self.details
        return response


class EntityNotFoundError(AppException):
    """Entidade não encontrada no banco de dados"""
    status_code = status.HTTP_404_NOT_FOUND
    default_message = "Recurso não encontrado"


class DuplicateEntityError(AppException):
    """Tentativa de criar entidade duplicada"""
    status_code = status.HTTP_409_CONFLICT
    default_message = "Recurso já existe"


class UnauthorizedError(AppException):
    """Usuário não autorizado para a ação"""
    status_code = status.HTTP_403_FORBIDDEN
    default_message = "Acesso negado"


class InvalidCredentialsError(AppException):
    """Credenciais inválidas"""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = "Credenciais inválidas"


class ValidationError(AppException):
    """Erro de validação de dados de negócio"""
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    default_message = "Dados inválidos"

