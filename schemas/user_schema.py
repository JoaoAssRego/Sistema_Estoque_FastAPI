from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel): # Modelo base para usuário
    occupation: str
    name: str
    email: str
    password: str
    admin: Optional[bool] = False
    active: Optional[bool]

    class Config: # Configuração para trabalhar com ORM
        from_attributes = True