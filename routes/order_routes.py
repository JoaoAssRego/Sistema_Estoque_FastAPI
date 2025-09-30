from fastapi import APIRouter, Depends, HTTPException
from models import Order, db
from .dependencies import session_dependencies
from schemas.order_schema import OrderBase
from sqlalchemy.orm import Session
order_router = APIRouter(prefix="/order", tags=["order"])  # Prefixo para todas as rotas de pedido

@order_router.get("/orders")
async def get_orders():
    return {"Esses são meus pedidos"}

@order_router.post("/create_order")
async def create_order(order_base: OrderBase, session: Session = Depends(session_dependencies)):
    order = session.query(Order).filter(Order.product_name == order_base.product_name).first() # Verifica se o produto já está cadastrado

    if order:
        raise HTTPException(status_code=400, detail="Order already registered, try another one") # Levanta um erro se o produto já existir
    else:
        new_order = Order(product_name=order_base.product_name, quantity=order_base.quantity, price=order_base.price) # Cria um novo pedido
        session.add(new_order) # Adiciona o novo pedido à sessão
        session.commit() # Salva as mudanças no banco de dados