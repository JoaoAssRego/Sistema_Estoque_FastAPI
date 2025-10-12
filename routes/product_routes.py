from fastapi import APIRouter, Depends, HTTPException, status
from models.models import Product, User, Category, Supplier
from .dependencies import session_dependencies, verify_token
from schemas.product_schema import ProductBase, JsonProductBase
from sqlalchemy.orm import Session
from typing import List

product_router = APIRouter(prefix="/product", tags=["product"],) # Prefixo para todas as rotas de produto

# Listar todos os produtos
@product_router.get("/", response_model=List[JsonProductBase])
async def list_products(session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    return session.query(Product).all()

@product_router.get("/{product_id}", response_model= JsonProductBase)
async def get_product(product_id: int, session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found!")    
    return product

@product_router.post("/create", response_model=JsonProductBase, status_code=status.HTTP_201_CREATED)
async def create_product(product_base: ProductBase, session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Only admins can create products")
    
    # valida duplicidade por nome (se nome for único)
    product = session.query(Product).filter(Product.name == product_base.name).first() # Verifica se o produto já está cadastrado
    
    if product:
         raise HTTPException(status_code=400, detail="Product already registered, try another one") # Levanta um erro se o produto já existir
    
    # opcional: validar FKs
    if product_base.category_id is not None:
        if not session.get(Category, product_base.category_id):
            raise HTTPException(status_code=404, detail="Category not found")
    if product_base.supplier_id is not None:
        if not session.get(Supplier, product_base.supplier_id):
            raise HTTPException(status_code=404, detail="Supplier not found")

    new_product = Product(
        name=product_base.name,
        description=product_base.description,
        price=product_base.price,
        category_id=product_base.category_id,
        supplier_id=product_base.supplier_id
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@product_router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    product = session.query(Product).filter(Product.id == product_id).first() # Verifica se o produto existe
    if not current_user.admin:
         raise HTTPException(status_code=403, detail="Only admins can delete products") # Apenas administradores podem deletar produtos
    if product:
         session.delete(product)
         session.commit()
         return {
             "message": f"O produto de id {product.id} foi deletado"
         }
    else:
         raise HTTPException(status_code=404, detail="Product not found!")