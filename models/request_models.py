from pydantic import BaseModel

class Recipe_model(BaseModel):
    title: str
    calories: int
    fat: float = 0.0
    sugar: float = 0.0
    salt: float = 0.0
    vegetarian: bool

class User_model(BaseModel):
    username: str
    password: str