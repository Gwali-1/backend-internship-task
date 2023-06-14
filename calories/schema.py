from pydantic import BaseModel
from datetime import date,time



class Setting(BaseModel):
    calorie_limit:float


    class Config:
        orm_mode=True


class Role(BaseModel):
    role:str


    class Config:
        orm_mode=True


class Record(BaseModel):
    id:int
    food_name:str
    calories:float
    date: date
    time:time
    below_lmit:bool


    class Config:
        orm_mode=True


class RecordCreate(BaseModel):
    food_name:str
    calories:float


    class Config:
        orm_mode=True


class UserCreate(BaseModel):
    email:str
    password:str

    class Config:
        orm_mode=True


class User(BaseModel):
    id:int
    email:str
    role: list[Role]
    settings: list[Setting]
    records_entered: list[Record]

    class Config:
        orm_mode=True





