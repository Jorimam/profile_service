from fastapi import FastAPI
from pydantic import BaseModel
from .base import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime, func 
from enum import Enum
from ..enums import Gender 


class User(Base):
    __tablename__ = 'users'

    id=Column(Integer, primary_key=True, nullable=False)
    username=Column(String(25), unique= True, nullable=False)
    email= Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False) 
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)