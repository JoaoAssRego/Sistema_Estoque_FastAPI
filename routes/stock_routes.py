from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import StockLevel, StockMovement, User, Product
from .dependencies import session_dependencies, verify_token, verify_admin
from schemas.stock_schema import (
    StockMovementGet, 
    StockMovementCreate,
    StockLevelGet,
    StockLevelPost, 
    StockLevelPatch, 
    StockLevelPut
)
from typing import List, Optional
from datetime import datetime

# stock_routes.py
stock_router = APIRouter(
    prefix="/stock",
    tags=['stock'],
    dependencies=[Depends(verify_admin)]
)

# ============================================
# STOCK LEVELS - Níveis de Estoque
# ============================================

@stock_router.get("/levels", response_model=List[StockLevelGet])
async def list_stock_levels(
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """Lista todos os níveis de estoque (apenas admin)"""
    return session.query(StockLevel).all()


@stock_router.get("/levels/{stock_id}", response_model=StockLevelGet)
async def get_stock_level(
    stock_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """Busca nível de estoque por ID (apenas admin)"""
    
    stocklevel = session.get(StockLevel, stock_id)
    if not stocklevel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock level not found!"
        )
    return stocklevel


@stock_router.post("/levels", response_model=StockLevelGet, status_code=status.HTTP_201_CREATED)
async def create_stock_level(
    stocklevel: StockLevelPost,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """Cria novo nível de estoque para um produto (apenas admin)"""
    
    # Valida se produto existe
    product = session.get(Product, stocklevel.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )
    
    # Verifica se já existe stock level para este produto
    existing = session.query(StockLevel).filter(
        StockLevel.product_id == product.id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Stock level already exists for this product!"
        )
    
    new_stocklevel = StockLevel(
        product_id=product.id,
        current_quantity=stocklevel.current_quantity,
        minimum_quantity=stocklevel.minimum_quantity,
        maximum_quantity=stocklevel.maximum_quantity,
        location=stocklevel.location
    ) 
    
    session.add(new_stocklevel)
    session.commit()
    session.refresh(new_stocklevel)
    return new_stocklevel


@stock_router.put("/levels/{stock_id}", response_model=StockLevelGet)
async def put_stock_level(
    stock_id: int,
    stock_update: StockLevelPut,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """Substitui completamente um nível de estoque (apenas admin)"""

    stocklevel = session.get(StockLevel, stock_id)
    if not stocklevel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock level not found!"
        )
    
    # Atualiza todos os campos
    stocklevel.current_quantity = stock_update.current_quantity
    stocklevel.minimum_quantity = stock_update.minimum_quantity
    stocklevel.maximum_quantity = stock_update.maximum_quantity
    stocklevel.location = stock_update.location
    
    session.commit()
    session.refresh(stocklevel)
    return stocklevel


@stock_router.patch("/levels/{stock_id}", response_model=StockLevelGet)
async def patch_stock_level(
    stock_id: int,
    stock_update: StockLevelPatch,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """Atualiza parcialmente um nível de estoque (apenas admin)"""

    stocklevel = session.get(StockLevel, stock_id)
    if not stocklevel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock level not found!"
        )
    
    # Atualiza apenas campos enviados
    update_data = stock_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # Aplica atualizações
    for key, value in update_data.items():
        setattr(stocklevel, key, value)
    
    session.commit()
    session.refresh(stocklevel)
    return stocklevel


@stock_router.delete("/levels/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock_level(
    stock_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """Deleta um nível de estoque (apenas admin)"""

    stocklevel = session.get(StockLevel, stock_id)
    if not stocklevel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock level not found!"
        )
    
    session.delete(stocklevel)
    session.commit()


# ============================================
# STOCK MOVEMENTS - Movimentações de Estoque
# ============================================

@stock_router.get("/movements", response_model=List[StockMovementGet])
async def list_stock_movements(
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """Lista todas as movimentações de estoque (apenas admin)"""

    return session.query(StockMovement).all()


@stock_router.get("/movements/{movement_id}", response_model=StockMovementGet)
async def get_stock_movement_by_id(
    movement_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """Busca uma movimentação específica por ID (apenas admin)"""
    
    movement = session.get(StockMovement, movement_id)
    if not movement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock movement not found!"
        )
    return movement


@stock_router.get("/movements/product/{product_id}", response_model=List[StockMovementGet])
async def get_stock_movements_by_product(
    product_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """Lista todas as movimentações de um produto específico (apenas admin)"""
    
    # Valida se produto existe
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )
    
    stockmovements = session.query(StockMovement).filter(
        StockMovement.product_id == product_id
    ).all()
    
    if not stockmovements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movements found for this product!"
        )
    
    return stockmovements


@stock_router.post("/movements", response_model=StockMovementGet, status_code=status.HTTP_201_CREATED)
async def create_stock_movement(
    stockmovement: StockMovementCreate,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """
    Cria nova movimentação de estoque e atualiza automaticamente o StockLevel (apenas admin).
    """
    
    # Valida se produto existe
    product = session.get(Product, stockmovement.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )
    
    # Cria movimentação
    new_stockmovement = StockMovement(
        product_id = product.id,
        movement_type = stockmovement.movement_type,
        quantity = stockmovement.quantity,
        reference_type = stockmovement.reference_type,
        user_id = current_user.id,
        created_at = datetime.now()
    )
    session.add(new_stockmovement)
    
    # Atualiza ou cria nível de estoque
    stock_level = session.query(StockLevel).filter(
        StockLevel.product_id == product.id
    ).first()
    
    if not stock_level:
        # Cria registro se não existir
        stock_level = StockLevel(
            product_id=product.id,
            current_quantity=0,
            minimum_quantity=0,
            maximum_quantity=1000
        )
        session.add(stock_level)
        session.flush()  # garante que o stock_level tenha ID antes de atualizar
    
    # Ajusta quantidade
    if stockmovement.movement_type == 'in':
        stock_level.current_quantity += stockmovement.quantity
    elif stockmovement.movement_type == 'out':
        if stock_level.current_quantity < stockmovement.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock! Available: {stock_level.current_quantity}, Requested: {stockmovement.quantity}"
            )
        stock_level.current_quantity -= stockmovement.quantity
    
    session.commit()
    session.refresh(new_stockmovement)
    return new_stockmovement


@stock_router.delete("/movements/{movement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock_movement(
    movement_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """
    Deleta uma movimentação e REVERTE o estoque (apenas admin).
    
    """

    stockmovement = session.get(StockMovement, movement_id)
    if not stockmovement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock movement not found!"
        )
    
    # Reverte a movimentação no estoque
    stock_level = session.query(StockLevel).filter(
        StockLevel.product_id == stockmovement.product_id
    ).first()
    
    if stock_level:
        if stockmovement.movement_type == 'in':
            # Era entrada, agora remove do estoque
            stock_level.current_quantity -= stockmovement.quantity
            if stock_level.current_quantity < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot delete: would result in negative stock!"
                )
        elif stockmovement.movement_type == 'out':
            # Era saída, agora adiciona de volta ao estoque
            stock_level.current_quantity += stockmovement.quantity
    
    session.delete(stockmovement)
    session.commit()


# ============================================
# ROTAS AUXILIARES
# ============================================

@stock_router.get("/levels/product/{product_id}", response_model=StockLevelGet)
async def get_stock_level_by_product(
    product_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """Busca nível de estoque de um produto específico (apenas admin)"""
    
    # Valida se produto existe
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )
    
    stock_level = session.query(StockLevel).filter(
        StockLevel.product_id == product_id
    ).first()
    
    if not stock_level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock level not found for this product!"
        )
    
    return stock_level


@stock_router.get("/alerts", response_model=List[StockLevelGet])
async def get_low_stock_alerts(
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """
    Lista produtos com estoque abaixo do mínimo (apenas admin).
    """
    low_stock = session.query(StockLevel).filter(
        StockLevel.current_quantity <= StockLevel.minimum_quantity
    ).all()
    
    return low_stock