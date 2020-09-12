from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from db.base import SessionLocal, engine
from db.functions import get_db
from models.db_models import Recipe
from models.request_models import Recipe_model
from sqlalchemy.orm import Session
import json
from random import randint
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post('/create_recipe')
async def create_recipe(recipe: Recipe_model, request: Request):
    db = SessionLocal()
    
    username = str(request.cookies).split("username")[1].split("'")[2] # do not fucking judge me
    new_recipe = Recipe()
    new_recipe.created_by = username
    new_recipe.calories = recipe.calories
    new_recipe.fat = recipe.fat
    new_recipe.sugar = recipe.sugar
    new_recipe.salt = recipe.salt
    new_recipe.vegetarian = recipe.vegetarian
    new_recipe.likes = 0
    new_recipe.dislikes = 0
    rid = randint(1111111111,9999999999)
    new_recipe.rid = rid
    db.add(new_recipe)
    db.commit()
    return {"rid":rid}


@router.post('/file_test')
async def file_test(request: Request):
    print("hi")
    print(dir(request.body))
    print(dir(request.json))
    return {"msh": "hi"}

    

@router.get('/create_recipe')
async def create_recipe_get(request: Request):
    return templates.TemplateResponse("create_recipe.html",{"request":request})

@router.get('/view_recipe/{rid}')
async def view_recipe(rid: int, request: Request):
    db = SessionLocal()
    vals = db.query(Recipe).filter(Recipe.rid==rid).first()
    # 'calories', 'created_by', 'date_created', 'dislikes',  'fat', 'id', 'likes', 'metadata', 'rid', 'salt', 'sugar', 'vegetarian'

    return templates.TemplateResponse("view_recipe.html",{"request":request,
                                                          "calories":vals.calories,
                                                          "created_by": vals.created_by,
                                                          "date_created":vals.date_created,
                                                          "fat":vals.fat,
                                                          "salt":vals.salt,
                                                          "sugar":vals.sugar,
                                                          "vegetarian":vals.vegetarian,
                                                          "likes":vals.likes,
                                                          "dislikes":vals.dislikes})
