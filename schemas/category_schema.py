from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel): # Modelo base para category
    name: str
    description: Optional[str]


    class Config: # Configuração para trabalhar com ORM
        from_attributes = True