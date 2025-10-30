from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Annotated
from datetime import datetime

class OrderCreate(BaseModel):
    """
    Schema para criar pedido.
    """
    product_id: int
    quantity: Annotated[int,Field(..., ge=0)]

    model_config = ConfigDict(from_attributes=True)


class JsonOrderGet(BaseModel):
    """Schema para retornar pedido completo"""
    id: int
    product_id: int
    user_id: int
    quantity: int
    total_price: float
    status: str
    created_at: Optional[datetime] = None  # se tiver no modelo

    model_config = ConfigDict(from_attributes=True)


class JsonOrderPut(BaseModel):
    """
    Schema para atualização completa do pedido.
    """
    product_id: int
    quantity: Annotated[int,Field(..., ge=0)]
    status: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator('status')
    @classmethod
    def valid_status(cls, v: str) -> str:
        valid_statuses = ["PENDING", "CONFIRMED", "DELIVERED", "CANCELED"]
        
        if v.upper() not in valid_statuses:
            raise ValueError(f"Status inválido. Use: {', '.join(valid_statuses)}")
        return v.upper()


class JsonOrderPatch(BaseModel):
    """Schema para atualização parcial do pedido"""
    product_id: Optional[int]
    quantity: Annotated[Optional[int],Field(..., ge=0)]
    status: Optional[str]

    model_config = ConfigDict(from_attributes=True)

    @field_validator('status')
    @classmethod
    def valid_status(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        valid_statuses = ["PENDING", "CONFIRMED", "DELIVERED", "CANCELED"]
        v_upper = v.upper()
        if v_upper not in valid_statuses:
            raise ValueError(f"Status inválido. Use: {', '.join(valid_statuses)}")
        return v_upper