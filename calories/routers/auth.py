from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_db_session, create_access_token
from .. import schema,database_actions
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi.responses import JSONResponse



router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

ACCESS_TOKEN_EXPIRE_MINUTES=30




@router.post("/create")
def create_user_account(user: schema.UserCreate, db: Session = Depends(get_db_session)):
    existing_user = database_actions.get_user_with_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Account with username already exist")
    new_user = database_actions.create_account(db, user)
    if new_user:
        return JSONResponse(status_code=200,content={"detail":"User account created successfully"})

    raise HTTPException(status_code=500, detail="Account could not be created at this moment")





@router.post("/login", response_model=schema.Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session=Depends(get_db_session)):
    data = {
        "username": form_data.username,
        "password": form_data.password
    }

    login_credentials =schema.UserLogin(**data)

    user = database_actions.login(db,login_credentials)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




