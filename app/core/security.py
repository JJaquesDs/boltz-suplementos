import bcrypt
import jwt
from uuid import UUID
from typing import Any
from datetime import timedelta, datetime, timezone

from app.core.config import settings


class PasswordHasher:
    """Classe para gerenciar hash de senhas com bcrypt"""

    @staticmethod
    def hash(password: str) -> str:
        """Método para gerar hash de senha"""

        # Transformando em utf-8 para o bcrypt trabalhar
        password_bytes = password.encode("utf-8")

        # Gerando valor aleatório antes do hash
        salt = bcrypt.gensalt()

        # Criando o hash
        hashed = bcrypt.hashpw(password_bytes, salt)

        # Devolvendo senha como utf-8
        return hashed.decode("utf-8")

    @staticmethod
    def verify(senha_simples: str, senha_hashed: str) -> bool:
        """Método para verificar senhas"""

        return bcrypt.checkpw(
            password=senha_simples.encode("utf-8"),
            hashed_password=senha_hashed.encode("utf-8")
        )


class JWTManipulador:
    """Gerenciador de tokens JWT"""

    @staticmethod
    def create_acess_token(
            user_id: UUID,
            expires_time: timedelta | None = None
    ) -> str:
        """Cria um token de acesso assinado JWT"""

        # Usa UTC para consistência
        agora = datetime.now(timezone.utc)

        if expires_time:
            expire = agora + expires_time
        else:
            expire = agora + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        payload = {
            "exp": expire,
            "iat": agora,
            "sub": str(user_id)
        }

        return jwt.encode(
            payload=payload,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        """Método que decodifica e valida token"""

        return jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

