from fastapi import APIRouter, Depends, HTTPException, status
from models.models import Supplier, User
from .dependencies import session_dependencies, verify_token
from schemas.supplier_schema import SupplierBase, JsonSupplierBase
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

supplier_router = APIRouter(prefix="/supplier", tags=["supplier"])

@supplier_router.get("/", response_model=List[JsonSupplierBase])
async def list_supplier(session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    return session.query(Supplier).all()

@supplier_router.get("/{supplier_id}", response_model=JsonSupplierBase)
async def get_supplier(supplier_id: int, session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    supplier = session.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found!")
    return supplier

@supplier_router.post("/", response_model=JsonSupplierBase, status_code=status.HTTP_201_CREATED)
async def create_supplier(supplier_base: SupplierBase, session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Only admins can create suppliers")

    existing = session.query(Supplier).filter(Supplier.name == supplier_base.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Supplier already exists")

    new_supplier = Supplier(name=supplier_base.name, contact_info=supplier_base.contact_info)
    session.add(new_supplier)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Supplier already exists")
    session.refresh(new_supplier)
    return new_supplier