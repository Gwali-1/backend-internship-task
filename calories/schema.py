from pydantic import BaseModel
from datetime import date,time



class Setting(BaseModel):
    calorie_limit:float



class Role(BaseModel):
    role:str



class Record(BaseModel):
    id:int
    food_name:str
    date: date
    time:time
    below_lmit:bool



class RecordCreate(BaseModel):
    food_name:str
    calories:float



class UserCreate(BaseModel):
    email:str
    password:str


class User(BaseModel):
    id:int
    email:str
    role: list[Role]
    settings: list[Setting]
    records_entered: list[Record]





