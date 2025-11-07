from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
    
class AuthBase(BaseModel): # Modelo para visualizar usuários
    email: str
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

class AuthChangePassword(BaseModel):
    password: str
    
    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

    @field_validator('password')
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
