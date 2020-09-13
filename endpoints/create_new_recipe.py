import os
import shutil
from fastapi import APIRouter, Depends, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from db.base import SessionLocal, engine
from db.functions import get_db
from models.db_models import Recipe
from models.request_models import Recipe_model
from sqlalchemy.orm import Session
from datetime import datetime
import json
from random import randint
from config import settings
from PIL import Image


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post('/create_recipe')
async def create_recipe(file: UploadFile = File(...), data: str = Form(...), request: Request = ""):
    
    db = SessionLocal()
    data = json.loads(data)
    # username = str(request.cookies).split("username")[1].split("'")[2] # do not fucking judge me
    username = data["username"]
    
    new_recipe = Recipe()
    new_recipe.created_by = username
    new_recipe.title = data["title"]
    new_recipe.calories = data["calories"]
    new_recipe.fat = data["fat"]
    new_recipe.sugar = data["sugar"]
    new_recipe.salt = data["salt"]
    new_recipe.vegetarian = data["vegetarian"]
    new_recipe.likes = 0
    new_recipe.dislikes = 0
    rid = randint(1111111111,9999999999)
    file_extension= str(file.filename).rsplit('.')[-1] # get file ext
    to_save = f"{rid}.{file_extension}"
    new_recipe.image_path = f"{settings.UPLOAD_FOLDER}{to_save}"
    new_recipe.rid = rid
    db.add(new_recipe)
    db.commit()
    upload_folder = settings.UPLOAD_FOLDER
    file_obj = file.file
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
    upload_file = os.path.join(upload_folder, to_save)

    # shutil.copyfileobj(file_obj, upload_folder)
    # upload_folder.close()

    # resize image and save
    output_size = (300, 300)
    i = Image.open(file_obj)
    i.thumbnail(output_size)
    i.save(upload_file)


    return {"rid":rid}
    


@router.get('/create_recipe')
async def create_recipe_get(request: Request):
    return templates.TemplateResponse("create_recipe.html",{"request":request})


@router.get('/view_recipe/{rid}')
async def view_recipe(rid: int, request: Request):
    db = SessionLocal()
    vals = db.query(Recipe).filter(Recipe.rid==rid).first()
    # 'calories', 'created_by', 'date_created', 'dislikes',  'fat', 'id', 'likes', 'metadata', 'rid', 'salt', 'sugar', 'vegetarian'
    diff = datetime.utcnow() - vals.date_created
    print(vals.image_path.split('/')[1])

    return templates.TemplateResponse("view_recipe.html",{"request":request,
                                                          "title":vals.title,
                                                          "calories":vals.calories,
                                                          "created_by": vals.created_by,
                                                          "date_created":diff.days,
                                                          "image_path":vals.image_path.split('/')[2],
                                                          "fat":vals.fat,
                                                          "salt":vals.salt,
                                                          "sugar":vals.sugar,
                                                          "vegetarian":vals.vegetarian,
                                                          "likes":vals.likes,
                                                          "dislikes":vals.dislikes})
