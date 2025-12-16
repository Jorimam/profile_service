from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.users import User
from datetime import datetime
import logging
import bcrypt
from ..schemas.auth import LoginRequest, LoginRespose
from ..auth.jwt import create_access_token

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginRespose)
def login(login_request:LoginRequest, db:Session = Depends(get_db)):
   user_exists = db.query(User).filter(User.email == login_request.email).first()
   if not user_exists:
        raise HTTPException(status_code=400, detail="Email does not exist")

    
   password_match = verify_passwords(login_request.password, user_exists.password)
   if not password_match:
        raise HTTPException(status_code=400, detail="Invalid password")



   claims = {
        'sub':str(user_exists.id),
        'email':user_exists.email,
        "user_id": str(user_exists.id)
    }

   access_token = create_access_token(claims)

   return LoginRespose(
        access_token = access_token,
        token_type="bearer",
        email= user_exists.email,
        user_id=user_exists.id   
    )

def verify_passwords(plain_text_password:str, hashed_password:str):
    # plain_text_password = plain_text_password.encode('utf-8')
    plain_text_password = plain_text_password.encode("utf-8")
    hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_text_password, hashed_password)

def raiseError(e):
    logger.error(f"failed to create record error: {e}")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail = {
            "status": "error",
            "message": f"failed to create user: {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )