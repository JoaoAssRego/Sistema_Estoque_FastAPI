from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import Order, Product, User
from .dependencies import session_dependencies, verify_token
from schemas.order_schema import OrderBase, JsonOrderBase
from typing import List 
order_router = APIRouter(prefix="/order", tags=["order"])

# Listar todos os pedidos
@order_router.get("/", response_model=List[JsonOrderBase])
async def list_order(session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    return session.query(Order).all()

@order_router.get("/{order_id}", response_model=JsonOrderBase)
async def get_order(order_id: int, session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found!")    
    return order
        

@order_router.post("/create", response_model=JsonOrderBase, status_code=status.HTTP_201_CREATED)
async def create_order(order_base: OrderBase, session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):

    # Buscar produto e calcular total no servidor
    product = session.get(Product, order_base.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found in our Database")
    
    if order_base.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    
    if current_user.admin and getattr(order_base, "user_id", None):
        target_user_id = order_base.user_id
        new_order = Order(
        product_id=product.id,
        status="PENDING",
        user_id=target_user_id,
        quantity=order_base.quantity,
        total_price=float(product.price) * int(order_base.quantity),    
        ) # Permite que administradores criem pedidos para outros usuários
    else:
        target_user_id = current_user.id
        new_order = Order(
            product_id=product.id,
            status="PENDING",
            user_id=target_user_id,
            quantity=order_base.quantity,
            total_price=float(product.price) * int(order_base.quantity),
        ) # Usuários normais só podem criar pedidos para si mesmos
        
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

@order_router.post("/{order_id}/cancel", response_model=JsonOrderBase)
async def cancel_order(
     order_id: int,
     session: Session = Depends(session_dependencies),
     current_user: User = Depends(verify_token),
 ): # Cancela um pedido existente
     
    order = session.get(Order, order_id) # Verifica se o pedido existe
    if not order:
         raise HTTPException(status_code=404, detail="Order not found!")
    
    if not current_user.admin and order.user_id != current_user.id:
        # já autenticado, mas sem permissão
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to do that!")
    order.status = "CANCELED"
    session.commit()
    session.refresh(order)
    return order