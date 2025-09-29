from pydantic import BaseModel

class SupplierBase(BaseModel): # Modelo base para supplier
    name: str
    contact_info: str

    class Config: # Configuração para trabalhar com ORM
        from_attributes = True