from pydantic import BaseModel, ConfigDict
from typing import Optional

class OrderBase(BaseModel): # Modelo base para Order
    product_id: int
    status: Optional[str] = "pending"
    user_id: Optional[int] = None
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class JsonOrderGet(BaseModel):
    id: int
    product_id: int
    user_id: int
    quantity: int
    total_price: float
    status: str

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class JsonOrderPut(BaseModel):
    product_id: int
    quantity: int
    status: str

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class JsonOrderPatch(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    status: Optional[str] = None

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)