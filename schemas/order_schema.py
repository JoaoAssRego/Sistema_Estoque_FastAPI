from pydantic import BaseModel, ConfigDict
from typing import Optional

class OrderBase(BaseModel): # Modelo base para Order
    product_id: int
    status: Optional[str] = "pending"
    user_id: Optional[int] = None
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class JsonOrderBase(BaseModel):
    id: int
    product_id: int
    user_id: int
    quantity: int
    total_price: float
    status: str

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)