from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime

class JsonStockMovementCreate(BaseModel):
    """Schema para criar movimentação (input do usuário)"""
    product_id: int = Field(gt=0)
    movement_type: str = Field(max_length=3, description="'in' or 'out'")
    quantity: int = Field(gt=0)
    reference_type: Optional[str] = Field(None, max_length=6, description="'order' or 'return'")

    model_config = ConfigDict(from_attributes=True)

    @field_validator('movement_type')
    @classmethod
    def valid_movement_type(cls, v):
        if v.lower() not in ['in', 'out']:
            raise ValueError("movement_type must be 'in' or 'out'")
        return v.lower()

    @field_validator('reference_type')
    @classmethod
    def valid_reference_type(cls, v): 
        if v is not None and v.lower() not in ['order', 'return']:
            raise ValueError("reference_type must be 'order' or 'return'")
        return v.lower() if v else v

class JsonStockMovementGet(BaseModel):
    """Schema para retornar movimentação (resposta do servidor)"""
    id: int
    product_id: int
    movement_type: str
    quantity: int
    user_id: int
    reference_type: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class JsonStockLevelGet(BaseModel):
    """Schema para retornar nível de estoque"""
    id: int
    product_id: int
    current_quantity: int
    minimum_quantity: int
    maximum_quantity: Optional[int] = None
    location: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
