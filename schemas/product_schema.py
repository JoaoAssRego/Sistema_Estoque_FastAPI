from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductBase(BaseModel): # Modelo base para Product
    name: str
    description: Optional[str] = None
    price: float
    category_id: int
    supplier_id: int

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class JsonProductBase(BaseModel): # Modelo para visualizar produtos
    id: int
    name: str
    description: str
    price: float
    category_id: int
    supplier_id: int

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
