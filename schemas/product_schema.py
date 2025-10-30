from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Annotated

class ProductBase(BaseModel): # Modelo base para Product
    name: Annotated[str,Field(
        max_length=120,
        pattern=r'^[a-zA-Z\s\^~]+$'
    )]
    description: Annotated[Optional[str],Field(
        max_length=350,
        pattern=r'^[a-zA-Z\s\^~]+$'
    )]
    price: float
    category_id: int
    supplier_id: int

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

    @field_validator('name')
    @classmethod
    def name_must_not_be_empy(cls,v: str) -> str:
        if v.lower() is None or v.lower() == "":
            raise ValueError("Name must not be empty or None")
        return v

class JsonProductGet(BaseModel): # Modelo para visualizar produtos
    id: int
    name: str
    description: str
    price: float
    category_id: int
    supplier_id: int

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class JsonProductPatch(BaseModel): # Modelo para Update em produtos
    name: Annotated[Optional[str],Field(
        max_length=120,
        pattern=r'^[a-zA-Z\s\^~]+$'
    )]
    description: Annotated[Optional[str],Field(
        max_length=350,
        pattern=r'^[a-zA-Z\s\^~]+$'
    )]
    price: Optional[float]
    category_id: Optional[int]
    supplier_id: Optional[int]

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
