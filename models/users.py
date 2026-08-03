import uuid

from enum import Enum

from sqlmodel import SQLModel, Field

from typing import Optional

from enums import user_role


class UserBase(SQLModel):
    """ Classe base de um Usuário para ser reutilizado no sistema """

    nome: str = Field(nullable=False, index=True, max_length=45)
    email: str = Field(nullable=False, index=True, max_length=45)
    role: Enum(user_role) = Field(nullable=False)


class Users(UserBase, table=True):
    """ Clase que vira tabela no banco de dados"""

    user_id: Optional[uuid] = Field(default=None, primary_key=True)
    senha: str = Field(nullable=False, max_length=45)


    

