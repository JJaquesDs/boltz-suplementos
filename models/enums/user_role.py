from enum import Enum


class UserRole(Enum):
    """ Classe de roles de usuários """

    USER = "user",
    SUPERUSER = "admin",
    ADMIN = "admin",
