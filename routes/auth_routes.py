from fastapi import APIRouter, Depends, HTTPException, status
from models.models import User
from .dependencies import session_dependencies, verify_token
from security.security import bcrypt_context
from schemas.user_schema import UserBase, UserCreate, UserPatch
from schemas.auth_schema import AuthBase
from sqlalchemy.orm import Session
from security.auth import create_token, auth
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def signup(user_base: UserCreate, session: Session = Depends(session_dependencies)):

    user = session.query(User).filter(User.email == user_base.email).first()

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    encrypted_password = bcrypt_context.hash(user_base.password)

    new_user = User(
        occupation=user_base.occupation,
        name=user_base.name,
        email=user_base.email,
        password=encrypted_password,
        admin=False,
        active=True
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    access_token = create_token(new_user.id)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "occupation": new_user.occupation,
        "access_token": access_token,
        "token_type": "bearer"
    }

@auth_router.post("/login")
async def login(auth_base: AuthBase, session: Session = Depends(session_dependencies)):

    user = auth(auth_base.email, auth_base.password, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    access_token = create_token(user.id)
    refresh_token = create_token(user.id, token_duration=60*24*7)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
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

@auth_router.get("/refresh")
async def useRefreshToken(user: User = Depends(verify_token)):
    access_token = create_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

