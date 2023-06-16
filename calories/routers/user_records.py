from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from ..dependencies import auth_token, get_db_session
from .. import schema,database_actions
from sqlalchemy.orm import Session
from typing import Annotated



router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/records", response_model=list[schema.Record])
def get_user_records(user_id: int = Depends(auth_token), db:Session = Depends(get_db_session)):
    records = database_actions.get_user_records(db,user_id)
    if not records:
        pass

    return records





@router.post("/add_record", response_model=schema.Record)
def add_record(record:schema.RecordCreate, user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    new_record = database_actions.add_record(db, record, user_id)
    if not new_record:
        return HTTPException( status_code=500 , detail="could not create record at this time")
    return new_record




@router.get("/get_record_by_limit/{limit}")
def get_record_by_limit(limit:bool, user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    pass


@router.get("/get_record_by_date")
def get_record_by_date(date:schema.Date, user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    pass


@router.get("/all_records")
def get_all_records( user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    pass

@router.delete("/delete_record")
def deleter_record(user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    pass
