from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel): # Modelo base para usuário
    occupation: str
    name: str
    email: str
    password: str
    active: Optional[bool]

    class Config: # Configuração para trabalhar com ORM
        from_attributes = True