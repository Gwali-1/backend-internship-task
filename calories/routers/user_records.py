from fastapi import APIRouter, Depends,Query
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from ..dependencies import auth_token, get_db_session,allowed_for_user_crud
from .. import schema,database_actions
from sqlalchemy.orm import Session
from typing import Annotated



router = APIRouter(
    prefix="/users",
    tags=["User"]
)

ALLOWED_ROLES = ["Regular", "Admin", "Manager"]

@router.get("/get_users", response_model=list[schema.User])
def get_user_records(user_id: int = Depends(auth_token), db:Session = Depends(get_db_session),page:Annotated[int|None,Query(ge=1)]=1, limit:Annotated[int|None, Query(ge=1,le=30)]=1):
    offset = (page - 1) * limit
    _ = allowed_for_user_crud(db,user_id)
    users = database_actions.get_users(db, offset, limit)
    return users






@router.get("/get_users_by_role/{role}", response_model=list[schema.User])
def get_record_by_limit(role:str, user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    print(role)
    _ = allowed_for_user_crud(db,user_id)
    users = database_actions.get_users_by_role(db,role)
    if not users:
        return []
    return users




@router.put("/change_role")
def change_user_role(role:schema.RoleUpdate, user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    if role.role not in ALLOWED_ROLES:
        raise HTTPException(status_code=500, detail="User cannot be assigned invalid role")
    _ = allowed_for_user_crud(db, user_id)

    changed_role = database_actions.change_user_role(db,role)
    if not changed_role:
        raise HTTPException(status_code=500, detail="Role could not be changed")
    return JSONResponse(status_code=200, content={"detail":"User role has been changed"})






@router.delete("/delete_user/{username}")
def deleter_record(username:str,user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    _ = allowed_for_user_crud(db,user_id)
    deleted = database_actions.delete_user_with_username(db,username)
    if not deleted:
        raise HTTPException(status_code=500, detail="Record could not be deleted")
    return JSONResponse(status_code=200, content={"detail":"Record has been deleted"})





@router.post("/create_user", response_model=schema.User)
def create_user(user:schema.UserCreate, user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    _ =  allowed_for_user_crud(db,user_id)
    new_user = database_actions.create_user(db,user)
    if not user:
        raise HTTPException(status_code=500, detail="something went wrong,could not create a new user a this time")
    return new_user



