from fastapi import FastAPI
from .database import engine
from .models.base import Base
import logging
from .routes.users import router as user_routes
from .routes.auth import router as auth_routes 
from fastapi.staticfiles import StaticFiles
from .routes.oauth import router as oauth_routes 
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
import os 

# app = FastAPI()


logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Profile Service App",
    version = "0.0.1",
    description = "Simple Upload..."
    )

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth_routes)
app.include_router(user_routes)
app.include_router(oauth_routes)
# app.include_router(profile_routes)


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "123"),
    https_only=False,
)
origins = ["http://localhost:8000",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Profile Service"
    }


