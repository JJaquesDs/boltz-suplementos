"""
=================================================================================
            Configurações da Aplicação - Boltz Suplementos
=================================================================================

Este arquivo carrega todas as configurações do sistema a partir do arquivo .env.
"""


import os

import secrets

import warnings

from pathlib import Path

from typing import Literal

from dotenv import load_dotenv


# ====================================================================================
# CARREGANDO .ENV
# ====================================================================================


CAMINHO_ENV = Path(r"C:\Users\joaov\Desktop\boltz_suplementos\.env")
load_dotenv(dotenv_path=CAMINHO_ENV, encoding="utf-8", override=True)


# ====================================================================================
# FUNÇÕES AUXILIARES
# ====================================================================================

def obter_env(chave: str, padrao: str = "") -> str:
    """Obtém variável de ambiente como string"""

    return os.getenv(chave, padrao)


def obter_env_obrigatorio(chave: str) -> str:
    """Obtém variável obrigatória (lança erro se não existir)"""

    valor = os.getenv(chave)
    if valor is None:
        raise ValueError(f"Variável obrigatória não encontrada: {chave}")
    return valor


def obter_bool(chave: str, padrao: bool = False) -> bool:
    """Converte variável para booleano"""

    valor = os.getenv(chave)
    if valor is None:
        return padrao
    return valor.lower() in ("true", "1", "yes", "on")


def obter_int(chave: str, padrao: int) -> int:
    """Converte variável para inteiro"""

    valor = os.getenv(chave)
    if valor is None:
        return padrao
    try:
        return int(valor)
    except ValueError:
        warnings.warn(f"Valor inválido para {chave}, usando padrão: {padrao}")
        return padrao


def obter_lista(chave: str, separador: str = ",") -> list[str]:
    """Converte variável separada por vírgulas em lista"""

    valor = os.getenv(chave, "")
    if not valor:
        return []
    return [item.strip() for item in valor.split(separador) if item.strip()]


# ====================================================================================
# CLASSE DE CONFIGURAÇÕES
# ====================================================================================

class Settings:
    """Configurações da aplicação carregadas via python-dotenv"""

    # Geral
    PROJECT_NAME: str = obter_env_obrigatorio("PROJECT_NAME")
    ENVIRONMENT: Literal["local", "staging", "production"] = obter_env("ENVIRONMENT", "local")  # type: ignore

    # API
    API_V1_STR: str = obter_env("API_V1_STR", "/")
    SECRET_KEY: str = obter_env("SECRET_KEY", secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = obter_int("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 8)

    # CORS (Cross-Origin Resource Sharing ou Compartilhamento de Recursos de Origem Cruzada)
    BACKEND_CORS_ORIGINS: list[str] = obter_lista("BACKEND_CORS_ORIGINS")

    # Banco de dados
    POSTGRES_SERVER: str = obter_env_obrigatorio("POSTGRES_SERVER")
    POSTGRES_PORT: int = obter_int("POSTGRES_PORT", 5432)
    POSTGRES_USER: str = obter_env_obrigatorio("POSTGRES_USER")
    POSTGRES_PASSWORD: str = obter_env("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = obter_env("POSTGRES_DB", "")

    # ------------------------------------------------------------
    # Segurança
    # ------------------------------------------------------------

    ALGORITHM: str = obter_env_obrigatorio("ALGORITHM")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Monta a URI do banco de dados. Ex: postgresql+psycopg://user:senha@host:5432/seu_banco_de_dados"""

        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # E-mail (ignorar por enquanto, sistema não vai usar)
    SMTP_TLS: bool = obter_bool("SMTP_TLS", True)
    SMTP_SSL: bool = obter_bool("SMTP_SSL", False)
    SMTP_PORT: int = obter_int("SMTP_PORT", 587)
    SMTP_HOST: str | None = obter_env("SMTP_HOST") or None
    SMTP_USER: str | None = obter_env("SMTP_USER") or None
    SMTP_PASSWORD: str | None = obter_env("SMTP_PASSWORD") or None
    EMAILS_FROM_EMAIL: str | None = obter_env("EMAILS_FROM_EMAIL") or None
    EMAILS_FROM_NAME: str | None = obter_env("EMAILS_FROM_NAME") or None

    @property
    def emails_enabled(self) -> bool:
        """Verifica se emails estão configurados"""

        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    # Primeiro Superusuario
    FIRST_SUPERUSER: str = obter_env_obrigatorio("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = obter_env_obrigatorio("FIRST_SUPERUSER_PASSWORD")

    # Monitoramento
    SENTRY_DSN: str | None = obter_env("SENTRY_DSN") or None

# ======================================================================================
# INSTÂNCIA GLOBAL
# ======================================================================================


settings = Settings()


"""
Instância única das configurações.

Use em toda a aplicação:
    from app.core.config import settings
"""
