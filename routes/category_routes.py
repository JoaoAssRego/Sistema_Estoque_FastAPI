from fastapi import APIRouter, Depends, HTTPException, status
from models.models import Category 
from .dependencies import session_dependencies,verify_token
from schemas.category_schema import CategoryBase, JsonCategoryBase
from sqlalchemy.orm import Session
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
    
@category_router.post("/create",response_model=JsonCategoryBase, status_code=status.HTTP_201_CREATED)
async def create_category(category_base: CategoryBase, session: Session = Depends(session_dependencies)):
    category = session.query(Category).filter(Category.name == category_base.name).first()
    if category:
        raise HTTPException(status_code=400, detail="Category already registered, try another one")
    category = Category(name=category_base.name, description=category_base.description)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category  # compatível com JsonCategoryBase

@category_router.post("/delete", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, session: Session= Depends(session_dependencies)):  # anotação corrigida
     category = session.query(Category).filter(Category.id == category_id).first()
     if category:
         session.delete(category)
         session.commit()
         return {
             "message": f"Category: {category_id} deleted!"
         }
     else:
         raise HTTPException(status_code=404, detail="Category not found!") # Levanta um erro se a categoria já existir
