from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr
from typing import Optional

class UserBase(BaseModel): # Modelo base para usuário
    occupation: str
    name: str
    email: EmailStr
    password: str
    admin: Optional[bool] = False
    active: Optional[bool]

    class Config: # Configuração para trabalhar com ORM
        from_attributes = True

class UserCreate(BaseModel): # Modelo base para autenticação

    occupation: str = Field(...,min_length=5, max_length=100)
    name: str = Field(...,min_length=5, max_length=100, pattern=r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$')
    email: EmailStr
    password: str = Field(...,min_length=5, max_length=100)

    model_config = ConfigDict(from_attributes=True)   

    @field_validator('occupation')
    @classmethod
    def occupation_not_empty(cls,v: str) -> str:
        """Valida ocupação"""
        if not v or not v.strip():
            raise ValueError("Ocupação não pode estar vazia")
        return ' '.join(v.split()).title()
    
    @field_validator('occupation')
    @classmethod
    def valid_occupation(cls, v: str) -> str:
        """Valida ocupação"""
        allowed_occupations = ['Manager', 'Sales', 'Warehouse', 'IT', 'HR','Packer']
        if v.title() not in allowed_occupations:
            raise ValueError(f"Ocupação inválida. Permitidas: {', '.join(allowed_occupations)}")
        return v.title()


    @field_validator('email')
    @classmethod
    def valid_email(cls, v: str) -> str:
        """Valida formato de email"""
        if ".com" not in v:
            raise ValueError("Email inválido")
        return v.lower().strip()
    
    @field_validator('name')
    @classmethod
    def name_not_empty(cls,v: str) -> str:
        """Valida nome"""
        if not v or not v.strip():
            raise ValueError("Nome não pode estar vazio")
        return ' '.join(v.split()).title()
    
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
    
class UserPatch(BaseModel): # Modelo para atualização parcial de usuários
    occupation: Optional[str] = Field(None, min_length=5, max_length=100)
    name: Optional[str] = Field(None, min_length=5, max_length=100, pattern=r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$')
    email: Optional[str] = Field(None, min_length=5, max_length=100, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    admin: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=5, max_length=100)
    active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
