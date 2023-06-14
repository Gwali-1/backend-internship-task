from fastapi import FastAPI
from .routers import auth
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app = FastAPI()


app.include_router(auth.router)

@app.get("/")
def home():
    return "home"

