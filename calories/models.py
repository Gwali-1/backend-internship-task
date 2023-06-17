from .database import Base
from sqlalchemy import Float, ForeignKey, Integer, String, Boolean, Column,Date,Time, func
from sqlalchemy.orm import relationship



class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String)
    password = Column(String)
    role = relationship("Roles")
    settings = relationship("UserSettings", cascade="all, delete")
    records_entered = relationship("CalorieRecords",cascade="all, delete")



class UserSettings(Base):
    __tablename__ = "user_settings"
    id = Column(Integer,primary_key=True,index=True)
    calorie_limit = Column(Float)
    user_id = Column(Integer,ForeignKey("users.id"), nullable=False)



class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer,primary_key=True,index=True)
    role = Column(String, default="Regular")
    user_id = Column(Integer,ForeignKey("users.id"), nullable=False)
    users = relationship("Users", back_populates="role")



class CalorieRecords(Base):
    __tablename__ = "records"
    id = Column(Integer,primary_key=True,index=True)
    food_name= Column(String)
    calories= Column(Float)
    date=Column(Date,default=func.date(func.now()))
    time=Column(Time, default=func.time(func.now()))
    owner = Column(Integer,ForeignKey("users.id"), nullable=False)
    below_limit = Column(Boolean,default=True)




