from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Schema para retorno do token"""
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    """Schema para requisição de login"""
    email: str
    password: str
