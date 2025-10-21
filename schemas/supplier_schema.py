from pydantic import BaseModel, ConfigDict
from typing import Optional

class SupplierBase(BaseModel): # Modelo base para supplier
    name: str
    contact_info: str

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class JsonSupplierBase(BaseModel): # Modelo para visualizar suppliers
    id: int
    name: str
    contact_info: str

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class JsonSupplierPatch(BaseModel): # Modelo para atualização parcial de suppliers
    name: Optional[str] = None
    contact_info: Optional[str] = None

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)