from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"]) # Prefixo para todas as rotas de autenticação

@auth_router.post("/login")
async def login():
    return {"message": "Login bem-sucedido"}
