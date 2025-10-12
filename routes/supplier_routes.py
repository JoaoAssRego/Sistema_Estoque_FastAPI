from fastapi import APIRouter, Depends, HTTPException
from models import Supplier, db
from .dependencies import session_dependencies
from schemas.supplier_schema import SupplierBase, JsonSupplierBase
from sqlalchemy.orm import Session
from typing import List
supplier_router = APIRouter(prefix="/supplier", tags=["supplier"]) # Prefixo para todas as rotas de supplier

@supplier_router.get("/", response_model=List[JsonSupplierBase])
async def list_supplier(session: Session = Depends(session_dependencies)):
    return session.query(Supplier).all()

@supplier_router.get("/{supplier_id}")
async def get_supplier(supplier_id: int, session: Session = Depends(session_dependencies)):
    supplier = session.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found!")    
    return supplier

@supplier_router.post("/")
async def create_supplier(supplier_base: SupplierBase, session: Session = Depends(session_dependencies)):
    supplier = session.query(Supplier).filter(Supplier.name == supplier_base.name).first() # Verifica se o supplier já está cadastrado
    if supplier:
        raise HTTPException(status_code=400, detail="Supplier already registered, try another one") # Levanta um erro se o supplier já existir
    else:
        new_supplier = Supplier(name=supplier_base.name, contact_info=supplier_base.contact_info) # Cria um novo supplier
        session.add(new_supplier) # Adiciona o novo supplier à sessão
        session.commit() # Salva as mudanças no banco de dados
    return {"message": f"Create a new category {supplier_base.name}"}