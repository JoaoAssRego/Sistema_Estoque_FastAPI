from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime

class OrderCreate(BaseModel):
    """
    Schema para criar pedido.
    
    O usuário envia apenas product_id e quantity.
    Status é sempre "PENDING" no backend.
    """
    product_id: int = Field(..., gt=0, description="ID do produto")
    quantity: int = Field(..., gt=0, description="Quantidade desejada")

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
    
    Usuários comuns só podem alterar quantity.
    Admins podem alterar status também.
    """
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    status: str = Field(..., description="Status do pedido")

    model_config = ConfigDict(from_attributes=True)

    @field_validator('status')
    @classmethod
    def valid_status(cls, v: str) -> str:
        valid_statuses = ["PENDING", "CONFIRMED", "DELIVERED", "CANCELED"]
        v_upper = v.upper()
        if v_upper not in valid_statuses:
            raise ValueError(f"Status inválido. Use: {', '.join(valid_statuses)}")
        return v_upper


class JsonOrderPatch(BaseModel):
    """Schema para atualização parcial do pedido"""
    product_id: Optional[int] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, gt=0)
    status: Optional[str] = None

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