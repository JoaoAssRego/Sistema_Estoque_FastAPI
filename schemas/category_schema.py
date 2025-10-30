from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional

class CategoryBase(BaseModel): # Modelo base para category
    name: str = Field(...,
        min_length=5, 
        max_length=100, 
        pattern=r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$'
    )
    description: Optional[str] = Field(
        max_length=350,
        pattern=r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$'
    )

    model_config= ConfigDict(from_attributes=True)

class JsonCategoryGet(BaseModel):
    id: int
    name: str
    description: str

    model_config= ConfigDict(from_attributes=True)

class JsonCategoryPatch(BaseModel):
    name: Optional[str] = Field(None,
        min_length=5, max_length=100, pattern=r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$'
    )
    description: Optional[str] = Field(None,
        max_length=350, pattern=r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$'
    )

    model_config= ConfigDict(from_attributes=True)