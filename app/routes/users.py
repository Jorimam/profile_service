from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schcemas.users import UserCreateRequest, UserUpdateRequest
from ..schcemas.users import User as UserResponse
from ..database import get_db
from ..models.users import User
from datetime import datetime
import logging
import bcrypt
import pymysql
from typing import List



logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create(user_request: UserCreateRequest, db: Session = Depends(get_db)):

    userExists = db.query(User).filter(
        (user_request.email == User.email)).first()

    if userExists:
        raiseError("user already exists")
    
    salts = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), salts)
    
    new_user = User(
        # **user_request.dict(exclude={"password", "confirm_password"}),
        username=user_request.username,
        email=user_request.email,
        password=hashed_password.decode(),
    )

    try:  
        db.add(new_user)  
        db.commit()
        db.refresh(new_user)

        return new_user
    except pymysql.DataError as e:
        raiseError(e)
    except Exception as e:
        raiseError(e)

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

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        
        raiseError(f"Failed to retrieve users: {e}")

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": f"User with id {user_id} not found",
                "timestamp": f"{datetime.utcnow()}"
            }
        )
    
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == user_id)

    if not user.first():
        raiseError(f"User with id {user_id} not found")

    try:
        user.delete(synchronize_session=False)
        db.commit()

        return {"message": "User deleted successfully"}
    except Exception as e:
        raiseError(f"Failed to delete user: {e}")



@router.patch("/{user_id}", response_model=UserResponse)
def partial_update_user(user_id: int, user_update: UserUpdateRequest, db: Session = Depends(get_db)):
    
    user_query = db.query(User).filter(User.id == user_id)
    existing_user = user_query.first()

    if not existing_user:
        raiseError(f"User with id {user_id} not found")
    
    
    update_data = user_update.model_dump(exclude_unset=True) 

    if 'gender' in update_data and update_data['gender'] is not None:
        update_data['gender'] = update_data['gender'].value
    if 'category' in update_data and update_data['category'] is not None:
        update_data['category'] = update_data['category'].value
    
    try:
        user_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(existing_user)
        
        return existing_user 
        
    except Exception as e:
        raiseError(f"Failed to patch update user: {e}")
