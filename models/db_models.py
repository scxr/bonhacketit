from db.base import Base
from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.types import DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from random import randint
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    rid = Column(Integer)
    created_by = Column(String)
    title = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow())
    calories = Column(Integer, default=0)
    fat = Column(Float, default=0.0)
    sugar = Column(Float, default=0.0)
    salt = Column(Float, default=0.0)
    vegetarian = Column(Boolean)
    image_path = Column(String)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,index=True, unique=True)
    hashed_pword = Column(String)
