from pydantic import BaseModel, ConfigDict
from typing import Optional

class CategoryBase(BaseModel): # Modelo base para category
    name: str
    description: Optional[str]

    model_config= ConfigDict(from_attributes=True)

class JsonCategoryBase(BaseModel):
    id: int
    name: str
    description: str

    model_config= ConfigDict(from_attributes=True)

class JsonCategoryPatch(BaseModel):
    name: Optional[str]
    description: Optional[str]

    model_config= ConfigDict(from_attributes=True)