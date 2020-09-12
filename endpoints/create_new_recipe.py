import os
import shutil
from fastapi import APIRouter, Depends, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from db.base import SessionLocal, engine
from db.functions import get_db
from models.db_models import Recipe
from models.request_models import Recipe_model
from sqlalchemy.orm import Session
import json
from random import randint
from config import settings


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post('/create_recipe')
async def create_recipe(file: UploadFile = File(...), data: str = Form(...), request: Request = ""):
    db = SessionLocal()
    data = json.loads(data)
    username = str(request.cookies).split("username")[1].split("'")[2] # do not fucking judge me
    new_recipe = Recipe()
    new_recipe.created_by = username
    new_recipe.calories = data["calories"]
    new_recipe.fat = data["fat"]
    new_recipe.sugar = data["sugar"]
    new_recipe.salt = data["salt"]
    new_recipe.vegetarian = data["vegetarian"]
    new_recipe.likes = 0
    new_recipe.dislikes = 0
    rid = randint(1111111111,9999999999)
    new_recipe.rid = rid
    db.add(new_recipe)
    db.commit()
    upload_folder = settings.UPLOAD_FOLDER
    file_obj = file.file
    upload_folder = open(os.path.join(upload_folder, file.filename), 'wb+')
    shutil.copyfileobj(file_obj, upload_folder)
    upload_folder.close()
    return {"rid":rid}
    

@router.post("/filetest")
def create_file(file: UploadFile = File(...), data: str = Form(...)):
    print(file)
    print(dir(data))
    data = json.loads(data)
    
    print(data["title"])
    upload_folder = settings.UPLOAD_FOLDER
    file_object = file.file
    #create empty file to copy the file_object to
    upload_folder = open(os.path.join(upload_folder, file.filename), 'wb+')
    shutil.copyfileobj(file_object, upload_folder)
    upload_folder.close()
    return {"filename": file.filename}


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
