from fastapi import APIRouter, Depends, HTTPException, status
from models.models import Category, User 
from .dependencies import session_dependencies,verify_token
from schemas.category_schema import CategoryBase, JsonCategoryBase
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

category_router = APIRouter(prefix="/category", tags=["category"]) # Prefixo para todas as rotas de produto

@category_router.get("/", response_model=List[JsonCategoryBase])
async def list_categories(session: Session = Depends(session_dependencies)):
    return session.query(Category).all()

@category_router.get("/{category_id}", response_model=JsonCategoryBase)
async def get_category(category_id: int, session: Session = Depends(session_dependencies)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found!")    
    return category
    
@category_router.post("/create", response_model=JsonCategoryBase, status_code=status.HTTP_201_CREATED)
async def create_category(category_base: CategoryBase, session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Only admins can create categories")
    category = session.query(Category).filter(Category.name == category_base.name).first()
    if category:
        raise HTTPException(status_code=400, detail="Category already registered, try another one")
    category = Category(name=category_base.name, description=category_base.description)
    session.add(category)
    try:
        session.commit()
    except IntegrityError: # Em caso de erro de integridade (e.g., duplicidade)
        session.rollback()
        # Em caso de corrida, respeita a constraint única
        raise HTTPException(status_code=409, detail="Category already exists")
    session.refresh(category)
    return category

@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete categories") # Apenas administradores podem deletar categorias
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found!") # Levanta um erro se a categoria não existir
    session.delete(category)
    session.commit()
    # 204 No Content: sem corpo
    return
