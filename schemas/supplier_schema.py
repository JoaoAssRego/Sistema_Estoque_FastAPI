from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional

class SupplierCreate(BaseModel): # Modelo base para supplier
    name: str = Field(
        max_length=120,
        pattern=r'^[a-zA-Z\s\^~]+$'# Regex para Alfabeto + Espaço
    )
    contact_info: str = Field(
        max_length=18, 
        description="Format: +XX XX XXXXXXXXX",
        # Regex para + seguido de 2 dígitos, espaço, 2 dígitos, espaço, 9 dígitos
        pattern=r'^\+\d{2}\s\d{2}\s\d{9}$' 
    )

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls,v: str) -> str:
        if v.lower() is None or v.lower() == "":
            raise ValueError("Name must not be empty or None")
        return v

    model_config = ConfigDict(from_attributes=True)

class SupplierBase(BaseModel): # Modelo para visualizar suppliers
    id: int
    name: str
    contact_info: str

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class SupplierPut(BaseModel): # Modelo para visualizar suppliers
    name: str = Field(
        max_length=120,
        pattern=r'^[a-zA-Z\s\^~]+$'
        ) # Regex para Alfabeto + Espaço

    contact_info: str = Field(
        max_length=18, 
        description="Format: +XX XX XXXXXXXXX",
        # Regex para + seguido de 2 dígitos, espaço, 2 dígitos, espaço, 9 dígitos
        pattern=r'^\+\d{2}\s\d{2}\s\d{9}$' 
        )

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class SupplierPatch(BaseModel): # Modelo para atualização parcial de suppliers
    name: Optional[str] = Field(
        max_length=120,
        pattern=r'^[a-zA-Z\s\^~]+$'
        ) # Regex para Alfabeto + Espaço
    
    contact_info: Optional[str] = Field(
        max_length=18, 
        description="Format: +XX XX XXXXXXXXX",
        # Regex para + seguido de 2 dígitos, espaço, 2 dígitos, espaço, 9 dígitos
        pattern=r'^\+\d{2}\s\d{2}\s\d{9}$' 
        )

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)