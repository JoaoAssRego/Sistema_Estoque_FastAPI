from fastapi import APIRouter, Depends, HTTPException
from models import Product, db
from .dependencies import session_dependencies
from schemas.product_schema import ProductBase, GetProductBase
from sqlalchemy.orm import Session

product_router = APIRouter(prefix="/product", tags=["product"]) # Prefixo para todas as rotas de produto

@product_router.post("/")
async def get_product(product_id: int, session: Session = Depends(session_dependencies)):
    if product_id != 0:
        return session.query(Product).all()
    else:
        return session.query(Product).filter(Product.id == get_product.id).first() # Retorna um produto específico

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