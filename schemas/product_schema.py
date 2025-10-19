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

class JsonProductGet(BaseModel): # Modelo para visualizar produtos
    id: int
    name: str
    description: str
    price: float
    category_id: int
    supplier_id: int

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class JsonProductPut(BaseModel): # Modelo para Update em produtos
    name: str
    description: str
    price: float
    category_id: int # Possível alterar, pois caso haja algum erro de escrita ou criação de uma categoria mais especifica
    supplier_id: int # Possível alterar, pois para o produto existe a possibilidade de mudar o fornedor

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class JsonProductPatch(BaseModel): # Modelo para Update em produtos
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None # Possível alterar, pois caso haja algum erro de escrita ou criação de uma categoria mais especifica
    supplier_id: Optional[int] = None # Possível alterar, pois para o produto existe a possibilidade de mudar o fornedor

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
