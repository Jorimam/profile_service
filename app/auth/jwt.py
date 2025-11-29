# from jose import  JWTError
from jose import jwt, JWTError
from typing import Optional
from datetime import timedelta, datetime
import bcrypt
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.users import User



SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'mysecretkey')
ALGORITHM = os.getenv('JWT_ALGORITHM','HS256')
ACCESS_TOKEN_EXPIRATION_MINUTES = int(os.getenv('JWT_EXPIRATION_TIME', 60))

def create_access_token(claims: dict, expires_delta: Optional[timedelta] = None) -> str:
    try:
        if expires_delta:
            expiration_time = datetime.utcnow() + expires_delta
        else:
            expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)


        claims.update({'exp': expiration_time})

        encoded_jwt = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt
    except JWTError as e:
        raise e

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token could not be validated")