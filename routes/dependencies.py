from fastapi import Depends, HTTPException
from security.security import SECRET_KEY, ALGORITHM
from models import db, User # Importa o engine do banco de dados
from sqlalchemy.orm import sessionmaker, Session # Importa sessionmaker para criar sessões
from jose import jwt,JWTError
# Dependência para fornecer uma sessão do banco de dados
def session_dependencies():
    try:
        Session = sessionmaker(bind=db)
        yield Session() # Fornece a sessão e o yield permite que o FastAPI gerencie o ciclo de vida da sessão
    finally:
        Session().close() # Garante que a sessão seja fechada após o uso


def verify_token(token, session: Session= Depends(session_dependencies)):
    # Verifica o token válido e extraí ID do usuário
    try:
        dict_info = jwt.decode(token,SECRET_KEY, ALGORITHM)
        user_id = dict_info.get("user_id")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    user = session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return user