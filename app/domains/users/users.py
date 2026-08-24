from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field

from typing import Optional

from app.domains.users.enums.user_role import UserRole


class UserBase(SQLModel):
    """ Classe base de um Usuário para ser reutilizado no sistema """

    nome: str = Field(nullable=False, index=True, max_length=45)
    email: str = Field(nullable=False, index=True, max_length=45)
    role: UserRole = Field(nullable=False)


class Users(UserBase, table=True):
    """ Clase que vira tabela no banco de dados"""

    __tablename__ = "Users"

    user_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    senha: str = Field(nullable=False, max_length=80)


    

