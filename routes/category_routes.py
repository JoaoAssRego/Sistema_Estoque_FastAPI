from fastapi import APIRouter, Depends, HTTPException
from models import Category, db
from .dependencies import session_dependencies
from schemas.category_schema import CategoryBase
from sqlalchemy.orm import Session

category_router = APIRouter(prefix="/category", tags=["category"]) # Prefixo para todas as rotas de produto

@category_router.post("/")
async def create_category(category_base: CategoryBase, session: Session = Depends(session_dependencies)):
    category = session.query(Category).filter(Category.name == category_base.name).first() # Verifica se a categoria já está cadastrada
    if category:
        raise HTTPException(status_code=400, detail="Category already registered, try another one") # Levanta um erro se a categoria já existir
    else:
        category = Category(name=category_base.name,description=category_base.description) # Cria uma nova categoria
        session.add(category) # Adiciona a nova categoria à sessão
        session.commit() # Salva as mudanças no banco de dados
    return {"message": f"Create a new category {category_base.name}"}