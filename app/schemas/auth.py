from pydantic import BaseModel, Field, EmailStr, field_validator
import re

class LoginRequest(BaseModel):
    email:EmailStr
    password:str=Field(min_lenght=6)


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



class LoginRespose(BaseModel):
    access_token:str 
    token_type:str='bearer'
    email:str 
    user_id:int