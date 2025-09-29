from fastapi import APIRouter, Depends, HTTPException
from models import Supplier, db
from ..dependencies import session_dependencies
from schemas.user_schema import Supplier_Base
from sqlalchemy.orm import Session

supplier_router = APIRouter(prefix="/supplier", tags=["supplier"]) # Prefixo para todas as rotas de supplier

@supplier_router.post("/")
async def create_supplier(supplier_base: Supplier_Base, session: Session = Depends(session_dependencies)):
    supplier = session.query(Supplier).filter(Supplier.name == supplier_base.name).first() # Verifica se o supplier já está cadastrado
    if supplier:
        raise HTTPException(status_code=400, detail="Supplier already registered, try another one") # Levanta um erro se o supplier já existir
    else:
        new_supplier = supplier(name=supplier_base.name,contact_info=supplier_base.contact_info) # Cria um novo supplier
        session.add(new_supplier) # Adiciona o novo supplier à sessão
        session.commit() # Salva as mudanças no banco de dados
    return {"message": f"Create a new category {supplier_base.name}"}