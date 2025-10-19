from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import Order, Product, User
from .dependencies import session_dependencies, verify_token
from schemas.order_schema import OrderBase, JsonOrderGet, JsonOrderUpdate
from typing import List 

order_router = APIRouter(prefix="/order", tags=["order"])

# Listar todos os pedidos
@order_router.get("/", response_model=List[JsonOrderGet])
async def list_order(session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    return session.query(Order).all()

@order_router.get("/{order_id}", response_model=JsonOrderGet)
async def get_order(
    order_id: int, 
    session: Session = Depends(session_dependencies), 
    current_user: User = Depends(verify_token)
):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found!")    
    return order

@order_router.post("/create", response_model=JsonOrderGet, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_base: OrderBase, 
    session: Session = Depends(session_dependencies), 
    current_user: User = Depends(verify_token)
):
    # Buscar produto e calcular total no servidor
    product = session.get(Product, order_base.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found in our Database")
    
    if order_base.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    
    # Determina user_id: admin pode criar para outros, usuário comum só pra si
    target_user_id = current_user.id
    if current_user.admin and getattr(order_base, "user_id", None):
        target_user_id = order_base.user_id
    
    new_order = Order(
        product_id=product.id,
        status="PENDING",
        user_id=target_user_id,
        quantity=order_base.quantity,
        total_price=float(product.price) * int(order_base.quantity),
    )
    
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

@order_router.post("/{order_id}/cancel", response_model=JsonOrderGet)
async def cancel_order(
    order_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token),
):
    # Busca o pedido diretamente
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found!")
    
    # Verifica permissão
    if not current_user.admin and order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to do that!")
    
    order.status = "CANCELED"
    session.commit()
    session.refresh(order)
    return order

@order_router.put("/{order_id}/update",response_model=JsonOrderGet,status_code=status.HTTP_200_OK)
async def put_order(
    order_id: int,
    order_update: JsonOrderUpdate, # Dados atualizados do pedido
    session: Session=Depends(session_dependencies),
    current_user: User=Depends(verify_token)
):
      # Valida que o id do corpo bate com o da URL
    if order_update.id != order_id:
        raise HTTPException(status_code=400, detail="Order ID mismatch between URL and body")
    
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found!")
    
    if not current_user.admin and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to do that!")
    
    if order_update.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0!")
    
    product = session.get(Product, order_update.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found!")
    
    # Atualiza todos os campos (PUT = substituição completa)
    order.product_id = order_update.product_id
    order.quantity = order_update.quantity
    order.status = order_update.status
    order.total_price = float(product.price) * int(order_update.quantity)
    # user_id não deve ser alterado (permanece o original)
    
    session.commit()
    session.refresh(order)
    return order

@order_router.patch("/{order_id}/update")
async def patch_order(
    order_id: int,
    order_update: JsonOrderUpdate,
    session: Session=Depends(session_dependencies),
    current_user: User=Depends(verify_token)    
):
    order = session.get(Order,order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Verifica permissão
    if not current_user.admin and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to do that!")
    
    needs_recalc = False # Indica se precisa recalcular total_price

    if order_update.product_id is not None:
        product = session.get(Product,order_update.product_id)
        if not product:
            raise HTTPException(status_code=404,detail="Product not found!")
        order.product_id = order_update.product_id
        needs_calc = True

    # Atualiza quantity se enviado
    if order_update.quantity is not None:
        if order_update.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than 0!")
        order.quantity = order_update.quantity
        needs_recalc = True
    
    if needs_calc:
        product = session.get(Product,order_update.product_id)
        order.total_price = float(product.price) * int(order.quantity)
    
    session.commit()
    session.refresh(order)
    return order

    
    
