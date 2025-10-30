from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional

class JsonProductGet(BaseModel): # Modelo para visualizar produtos
    id: int
    name: str
    description: str
    price: float
    category_id: int
    supplier_id: int

    # Permite ler de objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

# ========================================
# PRODUTO - CREATE
# ========================================

class ProductCreate(BaseModel):
    """Schema para criar produto"""
    name: str = Field(...,min_length=5, max_length=100, pattern=r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$')
    description: Optional[str] = Field(None,max_length=500)
    price: float = Field(None,gt=0)
    category_id: Optional[int] = Field(None,gt=0)
    supplier_id: Optional[int] = Field(None,gt=0)

    model_config = ConfigDict(from_attributes=True)

    @field_validator('name')
    @classmethod
    def normalize_name(cls, v: str) -> str:
        """Normaliza o nome: remove espaços extras e capitaliza"""
        if not v or not v.strip():
            raise ValueError('Nome não pode estar vazio')
        # Remove espaços extras e capitaliza primeira letra de cada palavra
        return ' '.join(v.split()).title()
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v: float) -> float:
        """Valida e normaliza preço"""
        if v > 1000000:
            raise ValueError('Preço parece irreal (máx: R$ 1.000.000)')
        # Arredonda para 2 casas decimais
        return round(v, 2)

# ========================================
# PRODUTO - UPDATE
# ========================================

class ProductUpdate(BaseModel):
    """Schema para atualizar produto (PUT - todos os campos)"""
    name: str = Field(...,min_length=5, max_length=100, pattern=r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$')
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    category_id: Optional[int] = Field(None, gt=0)
    supplier_id: Optional[int] = Field(None, gt=0)

    model_config = ConfigDict(from_attributes=True)

    @field_validator('price')
    @classmethod
    def round_price(cls, v: float) -> float:
        return round(v, 2)


class ProductPatch(BaseModel):
    """Schema para atualização parcial (PATCH - campos opcionais)"""
    name: Optional[str] = Field(None, min_length=5, max_length=100, pattern=r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$')
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    category_id: Optional[int] = Field(None, gt=0)
    supplier_id: Optional[int] = Field(None, gt=0)

    model_config = ConfigDict(from_attributes=True)

    @field_validator('name')
    @classmethod
    def normalize_name(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return ' '.join(v.split()).title()
        return v
    
    @field_validator('price')
    @classmethod
    def round_price(cls, v: Optional[float]) -> Optional[float]:
        if v is not None:
            return round(v, 2)
        return v