from pydantic import BaseModel, ConfigDict

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