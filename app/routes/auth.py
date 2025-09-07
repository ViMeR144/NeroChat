from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
	email: EmailStr
	password: str

class LoginRequest(BaseModel):
	email: EmailStr
	password: str

class TokenResponse(BaseModel):
	token: str

@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
	existing = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
	if existing:
		raise HTTPException(status_code=400, detail="Email already registered")
	user = User(email=payload.email, password_hash=hash_password(payload.password))
	db.add(user)
	db.commit()
	db.refresh(user)
	token = create_access_token(user.email)
	return TokenResponse(token=token)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
	user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
	if not user or not verify_password(payload.password, user.password_hash):
		raise HTTPException(status_code=401, detail="Invalid credentials")
	token = create_access_token(user.email)
	return TokenResponse(token=token)
