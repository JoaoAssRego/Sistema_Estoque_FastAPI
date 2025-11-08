from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
    
class Token(BaseModel):
    """Response do login/register"""
    access_token: str
    token_type: str = "bearer"
    user: dict  # ou UserMeResponse

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class UserMeResponse(BaseModel):
    """Response de /auth/me"""
    id: int
    name: str
    email: str
    occupation: str
    active: bool
    created_at: datetime
    
    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class AuthBase(BaseModel): # Modelo para visualizar usuários
    email: EmailStr
    password: str

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

    @field_validator('email')
    @classmethod
    def valid_email(cls, v: str) -> str:
        """Valida formato de email"""
        if '@' not in v or '.com' not in v:
            raise ValueError("Email inválido")
        return v.lower().strip()

class ChangePasswordRequest(BaseModel):
    """Request para trocar senha"""
    old_password: str
    new_password: str = Field(..., min_length=8)

    @field_validator('new_password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Valida força da senha"""
        if (len(v) < 8 or
            not any(c.islower() for c in v) or
            not any(c.isupper() for c in v) or
            not any(c.isdigit() for c in v) or
            not any(c in r'!@#$%^&*()-_=+[]{}|;:,.<>?/' for c in v)):
            raise ValueError("Senha fraca. Deve ter ao menos 8 caracteres, incluindo maiúsculas, minúsculas, números e símbolos.")
        return v
