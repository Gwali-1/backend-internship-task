from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from ..dependencies import auth_token, get_db_session,allowed_for_record_crud
from .. import schema,database_actions
from sqlalchemy.orm import Session



router = APIRouter(
    prefix="/calories",
    tags=["Records"]
)




@router.get("/user_records", response_model=list[schema.Record])
def get_user_records(user_id: int = Depends(auth_token), db:Session = Depends(get_db_session)):
    id = allowed_for_record_crud(db,user_id)
    records = database_actions.get_user_records(db,id)
    return records




@router.post("/add_record", response_model=schema.Record)
def add_record(record:schema.RecordCreate, user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    id = allowed_for_record_crud(db,user_id)
    new_record = database_actions.add_record(db, record, id)
    if not new_record:
        return HTTPException( status_code=500 , detail="could not create record at this time")
    return new_record





@router.get("/get_record_by_limit/{limit}", response_model=list[schema.Record])
def get_record_by_limit(limit:bool, user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    id = allowed_for_record_crud(db,user_id)
    records = database_actions.get_records_by_limit(db,id,limit)
    if not records:
        pass
    return records






@router.get("/all_records")
def get_all_records( user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    _ = allowed_for_record_crud(db,user_id)
    records = database_actions.get_all_records(db)
    if not records:
        pass
    return records







@router.delete("/delete_record/{record_id}")
def deleter_record(record_id:int,user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    _ = allowed_for_record_crud(db,user_id)
    deleted = database_actions.delete_record(db,record_id)
    if not deleted:
        return HTTPException(status_code=500, detail="Record could not be deleted")
    return JSONResponse(status_code=200, content={"detail":"Record has been deleted"})






@router.put("/change_calorie")
def change_calorie_record(calorie:schema.CalorieUpdate, user_id:int = Depends(auth_token), db:Session = Depends(get_db_session)):
    _ = allowed_for_record_crud(db, user_id)
    changed_role = database_actions.change_record_calorie(db,calorie)
    if not changed_role:
        raise HTTPException(status_code=500, detail="Calorie could not be Updated")
    return JSONResponse(status_code=200, content={"detail":"Calorie on record has been changed"})



