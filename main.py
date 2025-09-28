from fastapi import FastAPI
from routes.auth_routes import auth_router
from routes.order_routes import order_router
from utils.security import bcrypt_context

app = FastAPI(tittle="Inventory Management System", description="API for managing inventory, orders, and users", version="1.0.0")

app.include_router(auth_router)
app.include_router(order_router)   

## Para rodar o codigo e executar o servidor: uvicorn main:app --reload

