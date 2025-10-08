from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import Order, db  # corrigido o import
from .dependencies import session_dependencies, verify_token
from schemas.order_schema import OrderBase

order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verify_token)])  # Prefixo para todas as rotas de pedido

@order_router.get("/orders")
async def get_order():
    return {"Esses são meus pedidos"}

@order_router.post("/create_order")
async def create_order(order_base: OrderBase, session: Session = Depends(session_dependencies)):
    order = session.query(Order).filter(Order.product_name == order_base.product_name).first() # Verifica se o produto já está cadastrado

    if order:
        raise HTTPException(status_code=400, detail="Order already registered, try another one") # Levanta um erro se o produto já existir

    new_order = Order(
        product_name=order_base.product_name,
        quantity=order_base.quantity,
        price=order_base.price,
    ) # Cria um novo pedido
    session.add(new_order) # Adiciona o novo pedido à sessão
    session.commit() # Salva as mudanças no banco de dados
    session.refresh(new_order)
    return {
        "id": new_order.id,
        "product_name": new_order.product_name,
        "quantity": new_order.quantity,
        "price": new_order.price,
    }

@order_router.post("/cancel_order")
async def cancel_order(order_id: int, session: Session= Depends(session_dependencies)):
    order = session.query(Order).filter(Order.id == order_id).first() # Encontra pedido no Database
    if not order: # Caso não encontrado, retorna erro
        raise HTTPException(status_code=404, detail="Order not found in our Database")
    # corrigido: alterar a instância
    order.status = "CANCELED"
    session.commit()
    return {"message": f"Order {order_id} canceled with success", "order_id": order.id}