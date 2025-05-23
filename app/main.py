from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware 
import os
app = FastAPI()
  # Add blog here
from app.database import engine
from app.routers import user, dashboard
from app import models
models.Base.metadata.create_all(bind=engine)
# Mount static files (profile pictures)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")


# Routers
app.include_router(user.router)
app.include_router(dashboard.router)



# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SECRET_KEY", "your-very-secret-key"))
