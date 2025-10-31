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

