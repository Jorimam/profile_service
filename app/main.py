from fastapi import FastAPI
from .database import engine
from .models.base import Base
import logging
from .routes.users import router as user_routes



logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Profile Service App",
    version = "0.0.1",
    description = "Simple Upload..."
    )


# app.include_router(auth.router)
app.include_router(user_routes)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Hello world"
    }


