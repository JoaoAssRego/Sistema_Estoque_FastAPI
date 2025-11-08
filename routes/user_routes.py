from fastapi import APIRouter, Depends, HTTPException, status
from models.models import User, Order, StockMovement
from .dependencies import session_dependencies, verify_token, verify_admin
from security.security import bcrypt_context
from schemas.user_schema import UserBase, UserCreate, UserPatch
from schemas.auth_schema import AuthBase
from sqlalchemy.orm import Session
from security.auth import create_token, auth
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

user_router = APIRouter(
    prefix="/user", 
    tags=["user"],
    dependencies=[Depends(verify_admin)]
)

# ============================================
# USER - Lista de Usuários
# ============================================
@user_router.get("/list", response_model=List[UserBase])
async def listUsers(session: Session = Depends(session_dependencies)):
    return session.query(User).all()

@user_router.get("/{user_id}", response_model=UserBase)
async def getUser(
    user_id: int,
    session: Session = Depends(session_dependencies)
):
    user = session.get(User,user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found!"
        )
    return user

@user_router.patch("/{user_id}", response_model=UserBase)
async def update_user(
    user_id: int,
    user_update: UserPatch,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """
    Atualiza OUTRO usuário (apenas admin).
    
    Para atualizar seu próprio perfil, use PUT /auth/me
    """
    user = session.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Pega apenas campos enviados
    update_data = user_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo para atualizar"
        )
    
    # Validação: não pode trocar senha por aqui
    if 'password' in update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use POST /auth/change-password para trocar senha"
        )
    
    # Aplica atualizações
    for key, value in update_data.items():
        setattr(user, key, value)
    
    session.commit()
    session.refresh(user)
    
    return user

@user_router.put("/{user_id}/activate")
async def toggle_user_active(
    user_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """
    Ativa/desativa OUTRO usuário (apenas admin).
    """
    user = session.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Não pode desativar a si mesmo
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode desativar sua própria conta"
        )
    
    # Alterna status
    user.active = not user.active
    session.commit()
    
    status_msg = "ativado" if user.active else "desativado"
    
    return {
        "message": f"Usuário '{user.name}' {status_msg} com sucesso",
        "user_id": user.id,
        "active": user.active
    }

# ========================================
# DELEÇÃO (Admin)
# ========================================

@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: Session = Depends(session_dependencies),
    current_user: User = Depends(verify_token)
):
    """
    Remove OUTRO usuário permanentemente (apenas admin).
    """
    user = session.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Não pode deletar a si mesmo
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode deletar sua própria conta"
        )
    
    # Verifica se tem pedidos associados
    has_orders = session.query(Order).filter(Order.user_id == user_id).count() > 0
    if has_orders:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível deletar. Usuário tem pedidos associados. Desative a conta ao invés de deletar."
        )
    
    # Verifica se tem movimentações de estoque
    has_movements = session.query(StockMovement).filter(
        StockMovement.user_id == user_id
    ).count() > 0
    
    if has_movements:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível deletar. Usuário tem movimentações de estoque registradas. Desative a conta ao invés de deletar."
        )
    
    # Deleta
    session.delete(user)
    session.commit()