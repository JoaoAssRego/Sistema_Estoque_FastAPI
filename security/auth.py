from fastapi import APIRouter, Depends, HTTPException
from models.models import User, db
from routes.dependencies import session_dependencies
from sqlalchemy.orm import Session
from passlib.context import CryptContext

def create_token(users):
    token = f"kajdslakdj{users.id}"
    return token

def auth(email,password,session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif CryptContext.verify(password,user.password): # Verifica se a senha do usuario é a mesma contida no BD
        return False

    return user