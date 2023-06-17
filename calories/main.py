from fastapi import FastAPI
from .routers import auth,calorie_records,user_records
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(auth.router)
app.include_router(calorie_records.router)
app.include_router(user_records.router)

@app.get("/")
def home():
    return "home"

