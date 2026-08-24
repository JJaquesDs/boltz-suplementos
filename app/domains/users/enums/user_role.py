from enum import Enum


class UserRole(str, Enum):
    """ Classe de roles de usuários """

    USER = "user",
    SUPERUSER = "superuser",
    ADMIN = "admin",
