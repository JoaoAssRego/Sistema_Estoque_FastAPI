from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import StockLevel, StockMovement, User, Product
from .dependencies import session_dependencies, verify_token
from schemas.stock_schema import JsonStockLevelGet, JsonStockMovementGet, JsonStockMovementCreate, JsonStockLevelPost
from typing import List, Optional
from datetime import datetime
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

@stock_router.post("/levels",response_model=JsonStockLevelGet)
async def create_stock_levels(
    stocklevel: JsonStockLevelPost,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this information."
        )
    product = session.get(Product,stocklevel.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found!")
    new_stocklevel = StockLevel(
        product_id = product.id,
        current_quantity = stocklevel.current_quantity,
        minimum_quantity = stocklevel.minimum_quantity,
        location= stocklevel.location
    ) 
    session.add(new_stocklevel)
    session.commit()
    session.refresh(new_stocklevel)
    return new_stocklevel

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

@stock_router.get("/movement/{product_id}", response_model=List[JsonStockMovementGet])
async def get_stock_movement(
    product_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this information."
        )
    stockmovement = session.query(StockMovement).filter(StockMovement.product_id == product_id).all()
    if not stockmovement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movements found for this product!"
        )
    return stockmovement

@stock_router.post("/movement", response_model=JsonStockMovementGet, status_code=status.HTTP_201_CREATED)
async def create_stock_movement(
    stockmovement: JsonStockMovementCreate,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Only admins can create stock movements")
    
    product = session.get(Product, stockmovement.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found!")
    
    # Cria movimentação
    new_stockmovement = StockMovement(
        product_id=product.id,
        movement_type=stockmovement.movement_type,
        quantity=stockmovement.quantity,
        reference_type=stockmovement.reference_type,
        user_id=current_user.id,
        created_at=datetime.now()
    )
    session.add(new_stockmovement)
    
    # Atualiza nível de estoque
    stock_level = session.query(StockLevel).filter(StockLevel.product_id == product.id).first()
    if not stock_level:
        # Cria registro se não existir
        stock_level = StockLevel(
            product_id=product.id,
            current_quantity=0,
            minimum_quantity=0,
            maximum_quantity=1000
        )
        session.add(stock_level)
    
    # Ajusta quantidade
    if stockmovement.movement_type == 'in':
        stock_level.current_quantity += stockmovement.quantity
    elif stockmovement.movement_type == 'out':
        if stock_level.current_quantity < stockmovement.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock!")
        stock_level.current_quantity -= stockmovement.quantity
    
    session.commit()
    session.refresh(new_stockmovement)
    return new_stockmovement