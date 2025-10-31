from fastapi import APIRouter, Depends, HTTPException, status
from models.models import User
from .dependencies import session_dependencies, verify_token
from security.security import bcrypt_context
from schemas.user_schema import UserBase, UserCreate, UserPatch
from schemas.auth_schema import AuthBase
from sqlalchemy.orm import Session
from security.auth import create_token, auth
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/me", response_model=UserBase)
async def get_current_user(current_user: User = Depends(verify_token)):
    return current_user