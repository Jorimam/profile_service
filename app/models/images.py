from fastapi import FastAPI
from pydantic import BaseModel
import aiofiles




class ImageUploadRequest(BaseModel):
    __tablename__ = 'images'
    id:int 
    file_name:str 
    