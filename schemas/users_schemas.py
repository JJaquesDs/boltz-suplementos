import uuid

from enum import Enum

from models.users import UserBase

from models.enums import user_role

from typing import Optional


class UserCreate(UserBase):
    """ Schema para criar usuários """

    nome: str
    email: str
    role: Enum(user_role)
    senha: str


class UserPublic(UserBase):
    """ Classe pública para expor dados na API """

    user_id: uuid
    nome: str
    email: str
    role: Enum(user_role)


class UserReadSenha(UserBase):
    """ Classe para retornar um usuário com campo senha """

    user_id: uuid
    nome: str
    email: str
    senha: str
    role: Enum(user_role)


class UserUpdate(UserBase):
    """ Classe para atualizar um usuário """

    nome: Optional[str]
    email: Optional[str]
    senha: Optional[str]

