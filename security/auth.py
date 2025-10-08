import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from models.models import User, db
from routes.dependencies import session_dependencies
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from security.security import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, bcrypt_context

def create_token(user_id: int, token_duration: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=token_duration)
    payload = {"sub": str(user_id), "exp": int(expire.timestamp())}  # exp como UNIX timestamp
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def auth(email: str, password: str, session: Session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user