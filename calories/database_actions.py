
from fastapi import HTTPException
from . import models , schema
from sqlalchemy.orm import Session
from .dependencies  import hash_password, verify_password



def create_account(db:Session, user:schema.UserCreate):
    username =user.username
    password = user.password
    confirm_password = user.confirm_password

    if password != confirm_password:
        raise HTTPException(status_code=401, detail="passwords are not the same")
    new_user = models.Users(username=username, password=hash_password(password))
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        print(e)
        db.rollback()
        return False




def login(db:Session, user:schema.UserLogin):
    email = user.username
    password = user.password
    existing_user =  db.query(models.Users).filter(models.Users.email == email).first()
    if existing_user:
        if verify_password(password, existing_user.password):
             return existing_user
    return False



def get_user_with_username(db:Session, email:str):
    user = db.query(models.Users).filter(models.Users.email == email).first()
    if not user:
        return False
    return user

