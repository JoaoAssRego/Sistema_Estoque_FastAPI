from fastapi import APIRouter, Depends, HTTPException
from models import User, db
from .dependencies import session_dependencies
from security.security import bcrypt_context
from schemas.user_schema import UserBase
from schemas.auth_schema import AuthBase
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def criar_token(users):
    token = f"kajdslakdj{users.id}"
    return token

@auth_router.post("/")
async def home():
    return {"message": "Welcome to the authentication home page"}

@auth_router.post("/Signup")
async def signup(user_base: UserBase, session: Session = Depends(session_dependencies)):
    user = session.query(User).filter(User.email == user_base.email).first() # Verifica se o email já está cadastrado
    if user:
        raise HTTPException(status_code=400, detail="Email already registered, try another one") # Levanta um erro se o email já existir
    else:
        encrypted_password = bcrypt_context.hash(user_base.password) # Hash da senha para segurança
        new_user = User(occupation=user_base.occupation, name=user_base.name, email=user_base.email, password=encrypted_password) # Cria um novo usuário
        session.add(new_user) # Adiciona o novo usuário à sessão
        session.commit() # Salva as mudanças no banco de dados

@auth_router.post("/Login")
async def login(auth_base: AuthBase, session: Session = Depends(session_dependencies)):
    user = session.query(User).filter(User.email == auth_base.email).first() # Abre uma sessão no Banco de Dados e na tabela User para verificar se o email está cadastrado na tabela.
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    else:
        access_token = criar_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }



