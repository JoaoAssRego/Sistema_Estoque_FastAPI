from fastapi import FastAPI
from routes.auth_routes import auth_router
from routes.order_routes import order_router
from routes.product_routes import product_router
from routes.category_routes import category_router
from routes.supplier_routes import supplier_router
from routes.stock_routes import stock_router
from routes.user_routes import user_router

app = FastAPI(title="Inventory Management System", description="API for managing inventory, orders, and users", version="1.0.0")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(order_router)   
app.include_router(product_router)
app.include_router(category_router) 
app.include_router(supplier_router)
app.include_router(stock_router)


## Para rodar o codigo e executar o servidor: uvicorn main:app --reload

