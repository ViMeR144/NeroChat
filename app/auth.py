import os
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change")
JWT_ALG = "HS256"
JWT_EXP_MIN = int(os.getenv("JWT_EXP_MIN", "1440"))

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
http_bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
	return pwd_ctx.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
	return pwd_ctx.verify(password, password_hash)


def create_access_token(sub: str) -> str:
	exp = datetime.utcnow() + timedelta(minutes=JWT_EXP_MIN)
	payload = {"sub": sub, "exp": exp}
	return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def get_current_user_email(token: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)) -> str:
	if token is None:
		raise HTTPException(status_code=401, detail="Not authenticated")
	try:
		data = jwt.decode(token.credentials, JWT_SECRET, algorithms=[JWT_ALG])
		return data.get("sub")
	except JWTError:
		raise HTTPException(status_code=401, detail="Invalid token")
