from pydantic import BaseModel
from typing import Optional

class AuthBase(BaseModel): # Modelo base para autenticação
    email: str
    password: str

    class Config: # Configuração para trabalhar com ORM
        from_attributes = True