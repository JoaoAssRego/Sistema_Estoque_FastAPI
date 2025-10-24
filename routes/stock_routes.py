from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import StockLevel, StockMovement, User, Product
from .dependencies import session_dependencies, verify_token
from schemas.stock_schema import StockLevelBase, StockMovementBase 
from typing import List 

stock_router = APIRouter(prefix="/orders", tags=["orders"])

@stock_router("/", response_model=StockLevelBase)
def list_StockLevel(product_id: int = None,session: Session=Depends(session_dependencies),current_user: User= Depends(verify_token)):
    
    if not current_user.admin:
        raise HTTPException(detail=status.HTTP_403_FORBIDDEN,detail="Only admins can access this information.")
    if product_id != None:
        return session.query(StockLevel).filter(product_id)
    else:
        return session.query(st)