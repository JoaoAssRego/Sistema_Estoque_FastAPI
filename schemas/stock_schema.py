from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime

class StockMovementCreate(BaseModel):
    """Schema para criar movimentação"""
    product_id: int = Field(gt=0)
    movement_type: str = Field(description="'in' or 'out'")
    quantity: int = Field(gt=0)
    reference_type: Optional[str] = Field(None, max_length=20)

    model_config = ConfigDict(from_attributes=True)

    @field_validator('movement_type') # Validador para movement_type
    @classmethod # Método de classe
    def valid_movement_type(cls, v):
        if v.lower() not in ['in', 'out']:
            raise ValueError("movement_type must be 'in' or 'out'")
        return v.lower()  # normaliza para minúsculas

    @field_validator('reference_type')
    @classmethod
    def valid_reference_type(cls, v):
        if v is not None and v.lower() not in ['order', 'return']:
            raise ValueError("reference_type must be 'order' or 'return'")
        return v.lower() if v else v

class StockLevelBase(BaseModel):
    product_id: int 
    current_quantity: int = 0
    minimum_quantity: int = 0
    maximum_quantity: Optional[int] = None
    location: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class StockMovementBase(BaseModel):
    product_id: int
    movement_type: str
    quantity: int
    user_id: int
    reference_type: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
