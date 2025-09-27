from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"])  # Prefixo para todas as rotas de pedido

@order_router.get("/orders")
async def get_orders():
    return {"Esses são meus pedidos"}