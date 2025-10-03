import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from models.models import User, db
from routes.dependencies import session_dependencies
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from security.security import SECRET_KEY,ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM,bcrypt_context

def create_token(users_id): # JWT 
    expire_date = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user_id": str(users_id),
        "expire_date": int(expire_date.timestamp())
    }
    encoded_jwt = jwt.encode(payload,SECRET_KEY,ALGORITHM)

    return encoded_jwt

def auth(email,password,session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif bcrypt_context.verify(password,user.password): # Verifica se a senha do usuario é a mesma contida no BD
        return False

    return user