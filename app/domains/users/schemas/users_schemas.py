from uuid import UUID

from app.domains.users.users import UserBase

from app.domains.users.enums.user_role import UserRole

from pydantic import BaseModel, EmailStr

from typing import Optional


class UserCreate(BaseModel):
    """ Schema para criar usuários """

    nome: str
    email: EmailStr
    senha: str


class UserPublic(UserBase):
    """ Classe pública para expor dados na API """

    user_id: UUID
    nome: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True


class UserReadSenha(UserBase):
    """ Classe para retornar um usuário com campo senha """

    user_id: UUID
    nome: str
    email: EmailStr
    senha: str
    role: UserRole


class UserUpdate(BaseModel):
    """ Classe para atualizar um usuário """

    nome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]

