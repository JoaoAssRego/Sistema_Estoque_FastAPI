from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import Order, Product, User
from .dependencies import session_dependencies, verify_token, verify_admin
from schemas.order_schema import OrderCreate, JsonOrderGet, JsonOrderPatch, JsonOrderPut
from typing import List 

order_router = APIRouter(prefix="/order", tags=["order"],dependencies=[Depends(verify_admin)])

# ============================================
# GET - Listar todos os pedidos
# ============================================
@order_router.get("/", response_model=List[JsonOrderGet])
async def list_orders(
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """
    Lista pedidos:
    - Admin: vê todos os pedidos
    - Usuário comum: vê apenas seus pedidos
    """
    if current_user.admin:
        return session.query(Order).all()
    else:
        return session.query(Order).filter(Order.user_id == current_user.id).all()

# ============================================
# GET - Buscar pedido por ID
# ============================================
@order_router.get("/{order_id}", response_model=JsonOrderGet)
async def get_order(
    order_id: int, 
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found!"
        )
    
    return order

# ============================================
# POST - Criar novo pedido
# ============================================
@order_router.post("/", response_model=JsonOrderGet, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_base: OrderCreate, 
    session: Session = Depends(session_dependencies), 
    current_user: User = Depends(verify_token)
):
    # # Valida quantidade
    # if order_base.quantity <= 0:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Quantity must be greater than 0"
    #     )
    
    # Busca produto
    product = session.get(Product, order_base.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found in our database"
        )
    
    # Determina user_id: admin pode criar para outros, usuário comum só pra si
    target_user_id = current_user.id
    if getattr(order_base, "user_id", None):
        # Valida se o usuário alvo existe
        target_user = session.get(User, order_base.user_id)
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target user not found"
            )
        target_user_id = order_base.user_id
    
    # Cria pedido
    new_order = Order(
        product_id=product.id,
        status="PENDING",
        user_id=target_user_id,
        quantity=order_base.quantity,
        total_price=float(product.price) * order_base.quantity,
    )
    
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

# ============================================
# PATCH - Cancelar pedido
# ============================================
@order_router.patch("/{order_id}/cancel", response_model=JsonOrderGet)
async def cancel_order(
    order_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token),
):
    # Busca pedido
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found!"
        )
    
    # Verifica permissão
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this order"
        )

    # Valida se pode cancelar
    if order.status in ["DELIVERED", "CANCELED"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel order with status {order.status}"
        )
    
    # Cancela pedido
    order.status = "CANCELED"
    session.commit()
    session.refresh(order)
    return order

# ============================================
# PUT - Atualizar pedido completo
# ============================================
@order_router.put("/{order_id}", response_model=JsonOrderGet)
async def update_order(
    order_id: int,
    order_update: JsonOrderPut,  
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    # Busca pedido
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found!"
        )
    
    # Verifica permissão
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this order"
        )
    
    # Valida produto
    product = session.get(Product, order_update.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )
    
    # Atualiza apenas campos enviados
    update_data = order_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # Aplica atualizações
    for key, value in update_data.items():
        setattr(order, key, value)
    
    session.commit()
    session.refresh(order)
    return order

# ============================================
# PATCH - Atualizar pedido parcialmente
# ============================================
@order_router.patch("/{order_id}", response_model=JsonOrderGet)
async def partial_update_order(
    order_id: int,
    order_update: JsonOrderPatch,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)    
):
    # Busca pedido
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found!"
        )

    # Verifica permissão
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this order"
        )
    
    # Extrai apenas campos enviados
    update_data = order_update.model_dump(exclude_unset=True)
    
    # Se não há dados para atualizar
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    needs_recalc = False 
    product = None  
    
    # Valida e atualiza product_id se enviado
    if "product_id" in update_data:
        product = session.get(Product, update_data["product_id"])
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found!"
            )
        order.product_id = update_data["product_id"]
        needs_recalc = True

    if "status" in update_data: order.status = update_data["status"]

    # Recalcula total_price se necessário
    if needs_recalc:
        # Se não buscou produto ainda, busca agora
        if product is None:
            product = session.get(Product, order.product_id)
        
        order.total_price = float(product.price) * order.quantity
    
    session.commit()
    session.refresh(order)
    return order

# ============================================
# DELETE - Deletar pedido
# ============================================
@order_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    # Busca pedido
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found!"
        )
    
    # Deleta pedido
    session.delete(order)
    session.commit()
    # Não retorna nada com status 204