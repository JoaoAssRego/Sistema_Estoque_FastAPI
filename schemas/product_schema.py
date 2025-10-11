from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel): # Modelo base para Product
    name: str
    description: Optional[str] = None
    price: float
    category_id: int
    supplier_id: int

    class Config: # Configuração para trabalhar com ORM
        from_attributes = True

class GetProductBase(BaseModel): # Modelo para visualizar produtos
    id: Optional[int]