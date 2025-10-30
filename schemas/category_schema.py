from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Annotated

class CategoryBase(BaseModel): # Modelo base para category
    name: Annotated[str,Field(
        max_length=120,
        pattern=r'^[a-zA-Z\s\^~]+$'
    )]
    description: Annotated[Optional[str],Field(
        max_length=350,
        pattern=r'^[a-zA-Z\s\^~]+$'
    )]

    model_config= ConfigDict(from_attributes=True)

class JsonCategoryGet(BaseModel):
    id: int
    name: str
    description: str

    model_config= ConfigDict(from_attributes=True)

class JsonCategoryPatch(BaseModel):
    name: Optional[str]
    description: Optional[str]

    model_config= ConfigDict(from_attributes=True)