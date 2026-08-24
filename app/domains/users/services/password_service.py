from app.core.security import PasswordHasher


class PasswordService:
    """Classe para gerenciar operações com senhas"""

    def __init__(self):
        self.hasher = PasswordHasher

    def hash_password(self, password: str) -> str:
        """Criptografa uma senha"""

        return self.hasher.hash(password=password)

    def verify_password(
            self,
            senha_simples: str,
            hashed_password: str
    ) -> bool:
        """Verifica senhas corretas"""

        return self.hasher.verify(
            senha_simples=senha_simples,
            senha_hashed=hashed_password
        )

