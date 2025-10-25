from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import StockLevel, StockMovement, User, Product
from .dependencies import session_dependencies, verify_token
from schemas.stock_schema import JsonStockLevelGet, JsonStockMovementGet
from typing import List, Optional

stock_router = APIRouter(prefix="/stock", tags=['stock'])

@stock_router.get("/levels", response_model=List[JsonStockLevelGet])
async def list_stock_levels(
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this information."
        )
    else:
        return session.query(StockLevel).all()

@stock_router.get("/levels/{product_id}", response_model=JsonStockLevelGet)
async def get_stock_levels(
    product_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this information."
    )
    stocklevel = session.get(StockLevel, product_id)
    if not stocklevel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )
    return stocklevel
    
@stock_router.get("/movement",response_model=List[JsonStockMovementGet])
async def list_stock_movement(
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this information."
        )
    return session.query(StockMovement).all()

@stock_router.get("/movement/{product_id}", response_model=JsonStockLevelGet)
async def get_stock_levels(
    product_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this information."
    )
    stockmovement = session.get(StockMovement, product_id)
    if not stockmovement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )
    return stockmovement
    