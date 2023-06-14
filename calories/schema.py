from pydantic import BaseModel
from datetime import date,time

##################### token
class Token(BaseModel):
    access_token: str
    token_type: str


#user setting info
class Setting(BaseModel):
    calorie_limit:float


    class Config:
        orm_mode=True

#user role info
class Role(BaseModel):
    role:str


    class Config:
        orm_mode=True

#record info sent as response
class Record(BaseModel):
    id:int
    food_name:str
    calories:float
    date: date
    time:time
    below_lmit:bool


    class Config:
        orm_mode=True

#record info to create a record
class RecordCreate(BaseModel):
    food_name:str
    calories:float


    class Config:
        orm_mode=True

#user info to  create a user account
class UserCreate(BaseModel):
    username:str
    password:str
    confirm_password:str

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    username:str
    password:str

    class Config:
        orm_mode=True


#user info returned when requested
class User(BaseModel):
    id:int
    email:str
    role: list[Role]
    settings: list[Setting]
    records_entered: list[Record]

    class Config:
        orm_mode=True





