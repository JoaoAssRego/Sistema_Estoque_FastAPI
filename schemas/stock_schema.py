from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Annotated
from datetime import datetime

# ========================================
# STOCK MOVEMENT SCHEMAS
# ========================================

class StockMovementCreate(BaseModel):
    """Schema para criar movimentação"""
    product_id: Annotated[int,Field(..., gt=0)]
    movement_type: Annotated[str,Field(..., description="'in' ou 'out'")]
    quantity: Annotated[int,Field(..., gt=0)]
    reference_type: Annotated[Optional[str],Field(None, max_length=20)]

    model_config = ConfigDict(from_attributes=True)

    @field_validator('movement_type')
    @classmethod
    def valid_movement_type(cls, v: str) -> str:
        v_lower = v.lower()
        if v_lower not in ['in', 'out']:
            raise ValueError("movement_type deve ser 'in' ou 'out'")
        return v_lower

    @field_validator('reference_type')
    @classmethod
    def valid_reference_type(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v_lower = v.lower()
        valid_types = ['order', 'return', 'adjustment', 'manual']
        if v_lower not in valid_types:
            raise ValueError(f"reference_type inválido. Use: {', '.join(valid_types)}")
        return v_lower


class StockMovementGet(BaseModel):
    """Schema para retornar movimentação"""
    id: int
    product_id: int
    movement_type: str
    quantity: int
    user_id: int
    reference_type: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class StockMovementPut(BaseModel):
    product_id: int
    movement_type: Annotated[str,Field(max_length=3, description="'in' or 'out'")]
    quantity: Annotated[int,Field(gt=0)]
    reference_type: Annotated[str,Field(max_length=6, description="'order' or 'return'")]

    model_config = ConfigDict(from_attributes=True)

class StockMovementPatch(BaseModel):
    product_id: Optional[int]
    movement_type: Annotated[Optional[str],Field(max_length=3, description="'in' or 'out'")]
    quantity: Annotated[Optional[int],Field(gt=0)]
    reference_type: Annotated[Optional[str],Field(max_length=6, description="'order' or 'return'")]

    model_config = ConfigDict(from_attributes=True)

# ========================================
# STOCK LEVEL SCHEMAS
# ========================================

class StockLevelGet(BaseModel):
    """Schema para retornar nível de estoque"""
    id: int
    product_id: int
    current_quantity: int
    minimum_quantity: int
    maximum_quantity: Optional[int]
    location: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class StockLevelPost(BaseModel):
    """Schema para criar nível de estoque"""
    product_id: int = Field(..., gt=0)
    current_quantity: int = Field(default=0, ge=0)
    minimum_quantity: int = Field(default=0, ge=0)
    maximum_quantity: Optional[int] = Field(None, ge=0)
    location: Optional[str] = Field(None, max_length=60)

    model_config = ConfigDict(from_attributes=True)

    @field_validator('maximum_quantity')
    @classmethod
    def max_greater_than_min(cls, v: Optional[int], info) -> Optional[int]:
        """Valida que máximo é maior que mínimo"""
        if v is not None:
            min_qty = info.data.get('minimum_quantity', 0) # puxa o mínimo do mesmo input
            if v < min_qty:
                raise ValueError(f'Maximum Quantity ({v}) must be higher than minimum quantity ({min_qty})')
        return v


class StockLevelPut(BaseModel):
    """Schema para atualização completa (configurações apenas)"""
    current_quantity: int = Field(..., ge=0)
    minimum_quantity: int = Field(..., ge=0)
    maximum_quantity: Optional[int] = Field(None, ge=0)
    location: Optional[str] = Field(None, max_length=60)

    model_config = ConfigDict(from_attributes=True)


class StockLevelPatch(BaseModel):
    """Schema para atualização parcial (configurações apenas)"""
    minimum_quantity: Optional[int] = Field(None, ge=0)
    maximum_quantity: Optional[int] = Field(None, ge=0)
    location: Optional[str] = Field(None, max_length=60)

    model_config = ConfigDict(from_attributes=True)
