import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from models.models import User, db
from routes.dependencies import session_dependencies
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from security.security import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, bcrypt_context

def create_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": int(expire.timestamp())  # JWT padrão (timestamp UNIX)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def auth(email: str, password: str, session: Session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return None
    # Correção: retorna None se a senha NÃO confere
    if not bcrypt_context.verify(password, user.password):
        return None
    return user