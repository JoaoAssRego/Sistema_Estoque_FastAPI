from pydantic import BaseModel, ConfigDict
from typing import Optional

class StockMovementBase(BaseModel):
    product_id = int
    movement_type = str
    quantity = int
    reference_type = Optional[str]
    
    model_config = ConfigDict(from_attributes=True)

class StockLevelBase(BaseModel):
    product_id = int
    current_quantity = int
    minimum_quantity = int
    maximum_quantity = int
    location = str

    model_config = ConfigDict(from_attributes=True)
