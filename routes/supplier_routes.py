from fastapi import APIRouter, Depends, HTTPException, status
from models.models import Supplier, User, Product
from .dependencies import session_dependencies, verify_token
from schemas.supplier_schema import SupplierBase, JsonSupplierBase, JsonSupplierPatch
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

supplier_router = APIRouter(prefix="/supplier", tags=["supplier"])

# ============================================
# GET - Listar todos os fornecedores
# ============================================
@supplier_router.get("/", response_model=List[JsonSupplierBase])
async def list_suppliers(
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):

    return session.query(Supplier).all()

# ============================================
# GET - Buscar fornecedor por ID
# ============================================
@supplier_router.get("/{supplier_id}", response_model=JsonSupplierBase)
async def get_supplier(
    supplier_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):

    supplier = session.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found!"
        )
    return supplier

# ============================================
# POST - Criar novo fornecedor
# ============================================
@supplier_router.post("/", response_model=JsonSupplierBase, status_code=status.HTTP_201_CREATED)
async def create_supplier(
    supplier_base: SupplierBase,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):

    # Verifica permissão
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create suppliers"
        )

    # Valida duplicidade por nome
    existing = session.query(Supplier).filter(
        Supplier.name == supplier_base.name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Supplier with this name already exists"
        )

    # Cria novo fornecedor
    new_supplier = Supplier(
        name=supplier_base.name,
        contact_info=supplier_base.contact_info
    )
    
    session.add(new_supplier)
    
    try:
        session.commit()
        session.refresh(new_supplier)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Supplier already exists"
        )
    
    return new_supplier

# ============================================
# PUT - Atualizar fornecedor completamente
# ============================================
@supplier_router.put("/{supplier_id}", response_model=JsonSupplierBase)
async def update_supplier(
    supplier_id: int,
    supplier_update: SupplierBase,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):

    # Verifica permissão
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update suppliers"
        )
    
    # Busca fornecedor
    supplier = session.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found!"
        )

    # Valida duplicidade por nome (se mudou)
    if supplier_update.name != supplier.name:
        existing = session.query(Supplier).filter(
            Supplier.name == supplier_update.name,
            Supplier.id != supplier_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Another supplier with this name already exists"
            )

    # Atualiza campos
    supplier.name = supplier_update.name
    supplier.contact_info = supplier_update.contact_info

    try:
        session.commit()
        session.refresh(supplier)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Supplier name must be unique"
        )
    
    return supplier

# ============================================
# PATCH - Atualizar fornecedor parcialmente
# ============================================
@supplier_router.patch("/{supplier_id}", response_model=JsonSupplierBase)
async def partial_update_supplier(
    supplier_id: int,
    supplier_update: JsonSupplierPatch, 
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):

    # Verifica permissão
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update suppliers"
        )
    
    # Busca fornecedor
    supplier = session.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found!"
        )

    # Extrai dados enviados
    update_data = supplier_update.model_dump(exclude_unset=True)
    
    # Verifica se há dados para atualizar
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # Valida e atualiza name se enviado
    if "name" in update_data:
        new_name = update_data["name"]
        
        # Valida nome vazio
        if not new_name or not new_name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Supplier name cannot be empty"
            )
        
        # Valida duplicidade (se mudou)
        if new_name != supplier.name:
            existing = session.query(Supplier).filter(
                Supplier.name == new_name,
                Supplier.id != supplier_id
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Another supplier with this name already exists"
                )
        
        supplier.name = new_name

    # Atualiza contact_info se enviado
    if "contact_info" in update_data:
        supplier.contact_info = update_data["contact_info"]

    try:
        session.commit()
        session.refresh(supplier)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Supplier name must be unique"
        )
    
    return supplier

# ============================================
# DELETE - Deletar fornecedor
# ============================================
@supplier_router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(
    supplier_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):

    # Verifica permissão
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete suppliers"
        )
    
    # Busca fornecedor
    supplier = session.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found!"
        )
    
    # Verifica se há produtos associados
    products_count = session.query(Product).filter(
        Product.supplier_id == supplier_id
    ).count()
    
    if products_count > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot delete supplier. {products_count} product(s) are associated"
        )
    
    # Deleta fornecedor
    try:
        session.delete(supplier)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete supplier that has associated products"
        )