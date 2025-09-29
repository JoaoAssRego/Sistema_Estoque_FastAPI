from fastapi import APIRouter, Depends, HTTPException
from models import User, db
from ..dependencies import session_dependencies
from utils.security import bcrypt_context
from schemas.user_schema import UserBase
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/")
async def home():
    return {"message": "Welcome to the authentication home page"}

@auth_router.post("/Signup")
async def signup(user_base = UserBase, session: Session = Depends(session_dependencies)):
    user = session.query(User).filter(User.email == user_base.email).first() # Verifica se o email já está cadastrado
    if user:
        raise HTTPException(status_code=400, detail="Email already registered, try another one") # Levanta um erro se o email já existir
    else:
        encrypted_password = bcrypt_context.hash(user_base.password) # Hash da senha para segurança
        new_user = User(occupation=user_base.occupation, name=user_base.name, email=user_base.email, password=encrypted_password) # Cria um novo usuário
        session.add(new_user) # Adiciona o novo usuário à sessão
        session.commit() # Salva as mudanças no banco de dados


