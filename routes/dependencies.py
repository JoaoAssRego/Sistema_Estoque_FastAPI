from fastapi import Depends, HTTPException
from security.security import SECRET_KEY, ALGORITHM, oauth2_schema
from models.models import db, User  # corrigido
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError

# crie um SessionLocal reutilizável
SessionLocal = sessionmaker(bind=db, autocommit=False, autoflush=False)

def session_dependencies():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(session_dependencies)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # corrigido
        sub = payload.get("sub")  # o create_token usa 'sub'
        user_id = int(sub) if sub is not None else None
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token subject")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def verify_admin(current_user: User = Depends(verify_token)):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Only admins can access this resource")
    return current_user