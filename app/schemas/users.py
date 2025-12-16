from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, field_validator, model_validator, Field
from typing import Optional
import re
from ..enums import Gender 

class User(BaseModel):
    id:int 
    username: str
    email:EmailStr 


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str
    
class UserUpdateRequest(BaseModel):
    username:Optional[str]=None
    email:Optional[EmailStr]=None
    

    @field_validator('password')
    def validate_password(cls, value:str):
        if not re.search(r"[A-Z]", value):
            raise ValueError('password must contain atleast one capital letter')
        if not re.search(r"[a-z]", value):
            raise ValueError('password must contain atleast one lowercase letter')
        if not re.search(r"\d", value):
            raise ValueError('password must contain atleast one numeric value')
        if not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError('password must contain atleast one special character')
        return value
    
    @field_validator('username')
    def validate_name(cls, value:str):
        if not value.strip():
            raise ValueError("Ener a valid  name. Field cannot be empty")
        return value
     
    @model_validator(mode='after')
    def validate_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError('passwords must match')
        return self

