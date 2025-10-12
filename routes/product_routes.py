from fastapi import APIRouter, Depends, HTTPException
from models import Product,User, db
from .dependencies import session_dependencies, verify_token
from schemas.product_schema import ProductBase, JsonProductBase
from sqlalchemy.orm import Session
from typing import List

product_router = APIRouter(prefix="/product", tags=["product"], dependencies= [Depends(verify_token)]) # Prefixo para todas as rotas de produto

# Listar todos os produtos
@product_router.get("/", response_model=List[JsonProductBase])
async def list_products(session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    return session.query(Product).all()

@product_router.get("/{product_id}")
async def get_product(product_id: int, session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found!")    
    return product

@product_router.post("/create")
async def create_product(product_base: ProductBase, session: Session = Depends(session_dependencies)):
    product = session.query(Product).filter(Product.name == product_base.name).first() # Verifica se o produto já está cadastrado
    if product:
        raise HTTPException(status_code=400, detail="Product already registered, try another one") # Levanta um erro se o produto já existir
    else:
        # Verifica se a categoria e o fornecedor existem (pode ser implementado)
        new_product = Product(name=product_base.name, description=product_base.description, price=product_base.price, category_id=product_base.category_id, supplier_id=product_base.supplier_id) # Cria um novo produto
        session.add(new_product) # Adiciona o novo produto à sessão
        session.commit() # Salva as mudanças no banco de dados
        return {
        "id": new_product.id,
        "product_id": new_product.product_id,
        "quantity": new_product.quantity,
        "total_price": new_product.total_price,
        }

@product_router.post("/delete")
async def delete_product(order_id = int, session: Session = Depends(session_dependencies)):
    product = session.query(Product).filter(Product.id == order_id).first() # Verifica se o produto existe
    if product:
        session.delete(product)
        session.commit()
        return {
            "message": f"O produto de id {product.id} foi deletado"
        }
    else:
        raise HTTPException(status_code=404, detail="Product not found!")