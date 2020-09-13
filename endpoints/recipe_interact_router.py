from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from db.base import SessionLocal, engine
from db.functions import get_db
from models.db_models import Recipe
from models.request_models import Recipe_model
from sqlalchemy.orm import Session
import json
from datetime import datetime
from random import randint

router = APIRouter()

@router.post('/file_test')
async def file_test(request: Request):
    print(dir(request))

@router.post("/all_recipes")
async def view_all_recipes(db: Session = Depends(get_db)):
    cnt = 0
    all_vals = db.query(Recipe).all()
    data = {}
    for i in range(len(all_vals) -1, 0, -1):
        cnt+=1
        vals = all_vals[i]
        days_ago = datetime.utcnow() - vals.date_created 
        data[cnt] = {}
        data[cnt]["rid"] = vals.rid
        data[cnt]["created_by"] = vals.created_by
        data[cnt]["title"] = vals.title
        data[cnt]["date_created"] = days_ago.days
        data[cnt]["calories"] = vals.calories
        data[cnt]["fat"] = vals.fat
        data[cnt]["sugar"] = vals.sugar
        data[cnt]["salt"] = vals.salt
        data[cnt]["vegetarian"] = vals.vegetarian
        data[cnt]["image_path"] = vals.image_path
        data[cnt]["likes"] = vals.likes
        data[cnt]["dislikes"] = vals.dislikes
    return data

@router.post("/filter_recipes")
async def filter_recipes(request: Request):
    '''
    Expected params:
    Calories, Fat, Sugar, Salt
    '''
    cnt = 0
    print()
    db = SessionLocal()
    data_sent = await request.json()
    calories = data_sent["calories"]
    fat = data_sent["fat"]
    sugar = data_sent["sugar"]
    salt = data_sent["salt"]
    recipes = db.query(Recipe).filter(Recipe.calories<=calories).all()
    data = {}
    for i in range(len(recipes) - 1, 0, -1):
        cnt += 1
        passes = True
        vals = recipes[i]
        if vals.fat <= fat and vals.sugar <= sugar and vals.salt:
            diff = datetime.utcnow() - vals.date_created
            data[cnt] = {}
            data[cnt]["rid"] = vals.rid
            data[cnt]["created_by"] = vals.created_by
            data[cnt]["title"] = vals.title
            data[cnt]["image_path"] = vals.image_path
            data[cnt]["date_created"] = diff.days
            data[cnt]["calories"] = vals.calories
            data[cnt]["fat"] = vals.fat
            data[cnt]["sugar"] = vals.sugar
            data[cnt]["vegetarian"] = vals.vegetarian
            data[cnt]["likes"] = vals.likes
            data[cnt]["dislikes"] = vals.dislikes
    return data

'''
implement get all recipes endpoint done
somehow implement images
implement search with less than calories and stuff done
get users recipes endpoint (view user profile kind of thing)
'''
