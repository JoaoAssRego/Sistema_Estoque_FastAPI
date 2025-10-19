from fastapi import APIRouter, Depends, HTTPException, status
from models.models import Product, User, Category, Supplier
from .dependencies import session_dependencies, verify_token
from schemas.product_schema import ProductBase, JsonProductGet, JsonProductPut, JsonProductPatch
from sqlalchemy.orm import Session
from typing import List

product_router = APIRouter(prefix="/product", tags=["product"])

# ============================================
# GET - Listar todos os produtos
# ============================================
@product_router.get("/", response_model=List[JsonProductGet])
async def list_products(session: Session = Depends(session_dependencies)):
    return session.query(Product).all()

# ============================================
# GET - Buscar produto por ID
# ============================================
@product_router.get("/{product_id}", response_model=JsonProductGet)
async def get_product(product_id: int, session: Session = Depends(session_dependencies)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )
    return product

# ============================================
# POST - Criar novo produto
# ============================================
@product_router.post("/create", response_model=JsonProductGet, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_base: ProductBase,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    # Verifica se usuário é admin
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create products"
        )
    
    # Valida duplicidade por nome
    existing_product = session.query(Product).filter(
        Product.name == product_base.name
    ).first()
    
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product already registered, try another name"
        )
    
    # Valida Category FK (se fornecido)
    if product_base.category_id is not None:
        category = session.get(Category, product_base.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    
    # Valida Supplier FK (se fornecido)
    if product_base.supplier_id is not None:
        supplier = session.get(Supplier, product_base.supplier_id)
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found"
            )

    # Cria novo produto
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

# ============================================
# PUT - Atualizar produto completo
# ============================================
@product_router.put("/{product_id}", response_model=JsonProductGet)
async def update_product(
    product_id: int,
    product_update: JsonProductPut,  # Usando JsonProductPut
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    # Verifica se usuário é admin
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update products"
        )
    
    # Busca produto
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )
    
    # Valida Category FK (se fornecido)
    if product_update.category_id is not None:
        category = session.get(Category, product_update.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found!"
            )
        product.category_id = product_update.category_id
    else:
        product.category_id = None

    # Valida Supplier FK (se fornecido)
    if product_update.supplier_id is not None:
        supplier = session.get(Supplier, product_update.supplier_id)
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found!"
            )
        product.supplier_id = product_update.supplier_id
    else:
        product.supplier_id = None
    
    # Atualiza campos
    product.name = product_update.name
    product.description = product_update.description
    product.price = product_update.price
    
    session.commit()
    session.refresh(product)
    return product

# ============================================
# PATCH - Atualizar produto parcialmente
# ============================================
@product_router.patch("/{product_id}", response_model=JsonProductGet)
async def partial_update_product(
    product_id: int,
    product_update: JsonProductPatch,  # Schema com campos opcionais
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    # Busca produto
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )

    # Verifica permissão (apenas admin pode atualizar)
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update products"
        )
    
    # Atualiza apenas campos enviados (exclude_unset ignora campos None)
    update_data = product_update.model_dump(exclude_unset=True)
    # Se não há dados para atualizar
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # Valida Category se foi enviado
    if "category_id" in update_data:
        category = session.get(Category, update_data["category_id"])
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found!"
            )
    
    # Valida Supplier se foi enviado
    if "supplier_id" in update_data:
        supplier = session.get(Supplier, update_data["supplier_id"])
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found!"
            )
    
    # Valida price se foi enviado
    if "price" in update_data and update_data["price"] <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price must be greater than 0!"
        )
    
    # Aplica atualizações
    for key, value in update_data.items():
        setattr(product, key, value)
    
    session.commit()
    session.refresh(product)
    return product

# ============================================
# DELETE - Deletar produto
# ============================================
@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    # Verifica se usuário é admin
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete products"
        )
    
    # Busca produto
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )
    
    # Deleta produto
    session.delete(product)
    session.commit()
    # ✅ IMPORTANTE: Não retorna nada com status 204