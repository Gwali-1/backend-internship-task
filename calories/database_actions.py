from . import models , schema
from sqlalchemy.orm import Session
from .dependencies  import hash_password, verify_password
from datetime import datetime



def get_user_with_username(db:Session, username:str):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return False
    return user



def create_account(db:Session, user:schema.UserCreate):
    username =user.username
    password = user.password
    calorie_limit = user.limit
    new_user = models.Users(username=username, password=hash_password(password))
    db.add(new_user)
    #create user
    try:
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        return False

    user = get_user_with_username(db,username)
    if not user:
        return False

    #add role and limit setting
    new_role = models.Roles(user_id=user.id)
    db.add(new_role)
    limit_setting = models.UserSettings(calorie_limit=calorie_limit, user_id=user.id)
    db.add(limit_setting)

    try:
        db.commit()
        return new_user
    except:
        return False


#manager/admin
def change_setting(db:Session, limit:float, user_id:int):
    user_setting = db.query(models.UserSettings).filter(models.UserSettings.user_id == user_id).first()
    if not user_setting:
        return False
    user_setting.calorie_limit=limit
    try:
        db.commit()
        user=db.query(models.Users).filter(models.Users.id == user_id).first()
        return user
    except:
        db.rollback()
        return False



def login(db:Session, user:schema.UserLogin):
    username = user.username
    password = user.password
    existing_user =  db.query(models.Users).filter(models.Users.username == username).first()
    if existing_user:
        if verify_password(password, existing_user.password):
             return existing_user
    return False



#admin/manager
def get_users(db:Session, offset:int, limit:int):
    users = db.query(models.Users).offset(offset).limit(limit).all()
    return users

def get_users_by_role(db:Session, role:str):
    users = db.query(models.Users).join(models.Roles).filter(models.Roles.role == role).all()
    return users

def delete_user_with_username(db:Session,username:str):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    try:
        db.delete(user)
        db.commit()
        return True
    except:
        return False

def create_user(db:Session, user:schema.UserCreate):
    new_user = create_account(db,user)
    return new_user


def change_user_role(db:Session, new_role:schema.RoleUpdate):
    user_role = db.query(models.Roles).filter(models.Roles.user_id == new_role.user_id).first()
    user_role.role = new_role.role
    try:
        db.commit()
        db.refresh(user_role)
        return True
    except:
        return False










def check_if_below_limit(db:Session, user_id:int) -> bool:
    user_setting = db.query(models.UserSettings).filter(models.UserSettings.user_id == user_id).first()
    user_limit = user_setting.calorie_limit
    user_records = db.query(models.CalorieRecords).filter(models.CalorieRecords.owner==user_id, models.CalorieRecords.date == datetime.now().date()).all()
    if user_records:
        calories =[x.calories for x in user_records]
        check = sum(calories) < user_limit
        return check
    return True


#regular/admin
def add_record(db:Session, record:schema.RecordCreate, user_id:int):
    check = check_if_below_limit(db,user_id)
    new_record = models.CalorieRecords(**record.dict(), owner=user_id, below_limit=check)
    db.add(new_record)
    try:
        db.commit()
        db.refresh(new_record)
        return new_record
    except Exception as e:
        print(e)
        return False

def get_records_by_limit(db:Session, user_id:int, below_limit:bool):
    records = db.query(models.CalorieRecords).filter(models.CalorieRecords.owner == user_id, models.CalorieRecords.below_limit == below_limit).all()
    return records



def get_user_records(db:Session, user_id:int):
    records = db.query(models.CalorieRecords).filter(models.CalorieRecords.owner == user_id).all()
    return records



#admin / regular
def get_all_records(db:Session, offset:int, limit:int):
    records = db.query(models.CalorieRecords).offset(offset).limit(limit).all()
    return records




def delete_record(db:Session, record_id:int):
    user = db.query(models.CalorieRecords).filter(models.CalorieRecords.id == record_id).first()
    try:
        db.delete(user)
        db.commit()
        return True
    except:
        return False


def change_record_calorie(db:Session, new_calorie:schema.CalorieUpdate):
    record = db.query(models.CalorieRecords).filter(models.CalorieRecords.id == new_calorie.record_id).first()
    record.calories = new_calorie.calorie
    try:
        db.commit()
        db.refresh(record)
        return True
    except:
        return False







#create calorie reord/ before check for calories inserted that day
#when testing check if field is false


#get users
#create user
#deleete user
#get users by role,

#add record
#get records
#get records by user id , by time , date , below_limit


