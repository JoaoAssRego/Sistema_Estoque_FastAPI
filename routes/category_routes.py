from fastapi import APIRouter, Depends, HTTPException, status
from models.models import Category,Product, User 
from .dependencies import session_dependencies, verify_token
from schemas.category_schema import CategoryBase, JsonCategoryBase, JsonCategoryPatch
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

category_router = APIRouter(prefix="/category", tags=["category"])

# ============================================
# GET - Listar todas as categorias
# ============================================
@category_router.get("/", response_model=List[JsonCategoryBase])
async def list_categories(session: Session = Depends(session_dependencies)):

    return session.query(Category).all()

# ============================================
# GET - Obter categoria por ID
# ============================================
@category_router.get("/{category_id}", response_model=JsonCategoryBase)
async def get_category(
    category_id: int, 
    session: Session = Depends(session_dependencies)
):

    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found!"
        )    
    return category
    
# ============================================
# POST - Criar nova categoria
# ============================================
@category_router.post("/", response_model=JsonCategoryBase, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_base: CategoryBase, 
    session: Session = Depends(session_dependencies), 
    current_user: User = Depends(verify_token)
):

    # Verifica permissão
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only admins can create categories"
        )
    
    # Valida duplicidade por nome
    existing_category = session.query(Category).filter(
        Category.name == category_base.name
    ).first()
    
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Category already exists with this name"
        )
    
    # Cria nova categoria
    new_category = Category(
        name=category_base.name, 
        description=category_base.description
    )
    
    session.add(new_category)
    
    try:
        session.commit()
        session.refresh(new_category)
    except IntegrityError:
        # Fallback caso a validação acima falhe (race condition)
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Category already exists"
        )
    
    return new_category

# ============================================
# PUT - Atualizar categoria completamente
# ============================================
@category_router.put("/{category_id}", response_model=JsonCategoryBase)
async def update_category(
    category_id: int,
    category_update: CategoryBase,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):

    # Verifica permissão
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update categories"
        )
    
    # Busca categoria
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found!"
        )
    
    # Valida duplicidade de nome (se mudou)
    if category_update.name != category.name:
        existing = session.query(Category).filter(
            Category.name == category_update.name,
            Category.id != category_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Another category already exists with this name"
            )
    
    # Atualiza campos
    category.name = category_update.name
    category.description = category_update.description
    
    try:
        session.commit()
        session.refresh(category)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category name must be unique"
        )
    
    return category

# ============================================
# PATCH - Atualizar categoria parcialmente
# ============================================
@category_router.patch("/{category_id}", response_model=JsonCategoryBase)
async def partial_update_category(
    category_id: int,
    category_update: JsonCategoryPatch,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)    
):

    # Verifica permissão
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update categories"
        )
    
    # Busca categoria
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found!"
        )
    
    # Extrai apenas campos enviados
    update_data = category_update.model_dump(exclude_unset=True)
    
    # Se não há dados para atualizar
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # Valida duplicidade de nome se foi enviado
    if "name" in update_data:
        new_name = update_data["name"]
        
        # Não permite nome vazio
        if not new_name or not new_name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name cannot be empty"
            )
        
        # Valida duplicidade (se mudou)
        if new_name != category.name:
            existing = session.query(Category).filter(
                Category.name == new_name,
                Category.id != category_id
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Another category already exists with this name"
                )
        
        category.name = new_name
    
    # Atualiza description se enviado
    if "description" in update_data:
        category.description = update_data["description"]
    
    try:
        session.commit()
        session.refresh(category)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category name must be unique"
        )
    
    return category

# ============================================
# DELETE - Deletar categoria
# ============================================
@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int, 
    session: Session = Depends(session_dependencies), 
    current_user: User = Depends(verify_token)
):

    # Verifica permissão
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only admins can delete categories"
        )
    
    products_exist = session.query(Product).filter(
        Product.category_id == category_id
    ).first() is not None
    
    if products_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete category with products"
        )

    # Busca categoria
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found!"
        )
    
    try:
        session.delete(category)
        session.commit()
    except IntegrityError:
        # Falha se há produtos usando esta categoria
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete category that has associated products"
        )