from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import StockLevel, StockMovement, User, Product
from .dependencies import session_dependencies, verify_token
from schemas.stock_schema import StockLevelBase, StockMovementBase
from typing import List, Optional

stock_router = APIRouter(prefix="/stock", tags=['stock'])

@stock_router.get("/levels", response_model=List[StockLevelBase])
async def list_stock_levels(
    product_id: Optional[int] = None,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this information."
        )
    
    if product_id is not None:
        return session.query(StockLevel).filter(StockLevel.product_id == product_id).all()
    else:
        return session.query(StockLevel).all()

@stock_router.get("/movement",response_model=List[StockMovementBase])
async def list_stock_movement(
    product_id: Optional[int] = None,
    movement_type: Optional[str] = None,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this information."
        )
    
    if product_id is not None:
        return session.query(StockMovement).filter(StockMovement.product_id == product_id).all()
    elif movement_type is not None:
        if (movement_type == "entrada" or movement_type == "saida"):
            return session.query(StockMovement).filter(StockMovement.movement_type == movement_type).all()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Format of json incorrect!")
    else:
        return session.query(StockMovement).all()