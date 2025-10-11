from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import Order,Product,User, db
from .dependencies import session_dependencies, verify_token
from schemas.order_schema import OrderBase, GetOrderBase
from typing import List 
order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verify_token)])  # Prefixo para todas as rotas de pedido

# Listar todos os pedidos
@order_router.get("/", response_model=List[GetOrderBase])
async def list_order(session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    return session.query(Order).all()

@order_router.get("/{order_id}")
async def get_order(order_id: int, session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found!")    
    return order
        

@order_router.post("/create")
async def create_order(order_base: OrderBase, session: Session = Depends(session_dependencies), current_user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.product_id == order_base.product_id).first() # Verifica se o produto já está cadastrado

    # Buscar produto e calcular total no servidor
    product = session.get(Product, order_base.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found in our Database")
    
    new_order = Order(
        product_id=product.id,
        status="PENDING",
        user_id=current_user.id,
        quantity=order_base.quantity,
        total_price=float(product.price) * int(order_base.quantity),
    ) # Cria um novo pedido
    session.add(new_order) # Adiciona o novo pedido à sessão
    session.commit() # Salva as mudanças no banco de dados
    session.refresh(new_order)  # Atualiza a instância do pedido para refletir o estado atual do banco de dados
    return new_order

@order_router.post("/cancel")
async def cancel_order(order_id: int, session: Session= Depends(session_dependencies)):
    order = session.query(Order).filter(Order.id == order_id).first() # Encontra pedido no Database
    if not order: # Caso não encontrado, retorna erro
        raise HTTPException(status_code=404, detail="Order not found in our Database")
    # corrigido: alterar a instância
    order.status = "CANCELED"
    session.commit()
    return {"message": f"Order {order_id} canceled with success", "order_id": order.id}