from fastapi import APIRouter, Depends, HTTPException
from models import Product, db
from .dependencies import session_dependencies
from schemas.product_schema import ProductBase
from sqlalchemy.orm import Session

product_router = APIRouter(prefix="/product", tags=["product"]) # Prefixo para todas as rotas de produto

@product_router.post("/")
async def create_product(product_base: ProductBase, session: Session = Depends(session_dependencies)):
    product = session.query(Product).filter(Product.name == product_base.name).first() # Verifica se o produto já está cadastrado
    if product:
        raise HTTPException(status_code=400, detail="Product already registered, try another one") # Levanta um erro se o produto já existir
    else:
        # Verifica se a categoria e o fornecedor existem (pode ser implementado)
        new_product = Product(name=product_base.name, description=product_base.description, price=product_base.price, category_id=product_base.category_id, supplier_id=product_base.supplier_id) # Cria um novo produto
        session.add(new_product) # Adiciona o novo produto à sessão
        session.commit() # Salva as mudanças no banco de dados