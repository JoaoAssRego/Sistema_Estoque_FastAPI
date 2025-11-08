from fastapi import APIRouter, Depends, HTTPException, status
from models.models import User
from .dependencies import session_dependencies, verify_token
from security.security import bcrypt_context
from schemas.user_schema import UserBase, UserCreate, UserPatch
from schemas.auth_schema import AuthBase, ChangePasswordRequest, Token
from sqlalchemy.orm import Session
from security.auth import create_token, auth
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/me", response_model=UserBase)
async def get_current_user(current_user: User = Depends(verify_token)):
    return current_user

@auth_router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(session_dependencies)
):
    """
    Login - obter token JWT.
    """
    # Busca usuário
    user = session.query(User).filter(User.email == form_data.username).first()
    
    # Verifica credenciais
    if not user or not bcrypt_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verifica se está ativo
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    # Cria token
    access_token = create_token(user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "occupation": user.occupation,
            "active": user.active
        }
    }

@auth_router.post("/login_form")
async def login_form(request_form_schema: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(session_dependencies)):

    user = auth(request_form_schema.username, request_form_schema.password, session)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_token(user.id)
    refresh_token = create_token(user.id, token_duration=60*24*7)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@auth_router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserBase,
    session: Session = Depends(verify_token)
):
    """
    Registro - criar nova conta (auto-inscrição).
    
    Admins devem ser criados via POST /users (apenas por outros admins).
    """
    # Verifica duplicação
    existing = session.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Validação: não permite criar admin via registro público
    if user_data.admin == True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não é possível criar admin via registro público. Contate um administrador."
        )
    
    # Cria usuário (sempre como packer ou logistics_coordinator)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=bcrypt_context.hash(user_data.password),
        occupation=user_data.occupation,  # packer ou logistics_coordinator apenas
        active=True
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    # Cria token automaticamente
    access_token = create_token(new_user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "occupation": new_user.occupation,
            "active": new_user.active
        }
    }

@auth_router.get("/refresh")
async def useRefreshToken(current_user: User = Depends(verify_token)):
    access_token = create_token(current_user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@auth_router.post("/change-password")
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(verify_token),
    session: Session = Depends(session_dependencies)
):
    """
    Trocar senha do usuário logado.
    """
    # Verifica senha atual
    if not bcrypt_context.verify(password_data.old_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta"
        )
    
    # Atualiza senha
    current_user.password = bcrypt_context.hash(password_data.new_password)
    session.commit()
    
    return {"message": "Senha alterada com sucesso"}