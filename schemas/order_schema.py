from pydantic import BaseModel
from typing import Optional

class OrderBase(BaseModel): # Modelo base para Order
    product_id: int
    status: Optional[str] = "pending"
    user_id: Optional[int] = None
    quantity: int
    total_price: float

    class Config: # Configuração para trabalhar com ORM
        from_attributes = True