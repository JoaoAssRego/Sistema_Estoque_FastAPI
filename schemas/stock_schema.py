from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Annotated
from datetime import datetime

class JsonStockMovementCreate(BaseModel):
    """Schema para criar movimentação (input do usuário)"""
    product_id: Annotated[int,Field(strict=False)]
    movement_type: Annotated[str,Field(max_length=3, description="'in' or 'out'")]
    quantity: Annotated[int,Field(gt=0)]
    reference_type: Annotated[Optional[str],Field(None, max_length=6, description="'order' or 'return'")]

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
    reference_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class JsonStockLevelGet(BaseModel):
    """Schema para retornar nível de estoque"""
    id: int
    product_id: int
    current_quantity: int
    minimum_quantity: int
    maximum_quantity: int
    location: str

    model_config = ConfigDict(from_attributes=True)

class JsonStockLevelPost(BaseModel):
    """Schema para criar Stock Level"""
    product_id: int
    current_quantity: Annotated[int,Field(default=0,ge=0)]
    minimum_quantity: Annotated[int,Field(ge=0)]
    maximum_quantity: Annotated[int,Field(ge=0)]
    location: Annotated[Optional[str],Field(default=None,max_length=60,description="Product section")]

    model_config = ConfigDict(from_attributes=True)

    @field_validator('location')
    @classmethod
    def valid_location(cls,v):
        if v.lower() is None or v.lower() not in ['fridge','shelves','pallet truck']: # Places from stock
            raise ValueError("Location not exist in stock!")
        return v.lower()
    
    @field_validator('minimum_quantity')
    @classmethod
    def valid_minimum(cls,v):
        if cls.current_quantity < v:
            raise ValueError("Actual value cannot be lower than minimum") 
        return v
    
    @field_validator('maximum_quantity')
    @classmethod
    def valid_maximum(cls,v):
        if cls.current_quantity > v:
            raise ValueError("Actual value cannot be higher than maximum") 
        return v
    
class JsonStockLevelPut(BaseModel):
    current_quantity: Annotated[int,Field(default=0,ge=0)]
    minimum_quantity: Annotated[int,Field(ge=0)]
    maximum_quantity: Annotated[int,Field(ge=0)]
    location: Annotated[str,Field(max_length=60,description="Product section")]

class JsonStockLevelPatch(BaseModel):
    """Schema para alteração parcial do Stock"""
    product_id: int
    current_quantity: Annotated[Optional[int],Field(ge=0)]
    minimum_quantity: Annotated[Optional[int],Field(ge=0)]
    maximum_quantity: Annotated[Optional[int],Field(ge=0)]
    location: Annotated[Optional[str],Field(default=None,max_length=60,description="Product section")]
