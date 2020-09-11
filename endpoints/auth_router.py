from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from db.base import SessionLocal, engine
from sqlalchemy.orm import Session
from db.functions import get_db
from models.db_models import User
from models.request_models import User_model
import bcrypt
router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/register")
async def register(user: User_model, db: Session = Depends(get_db)):
    user_sent = User()
    user_sent.username = user.username
    user_sent.hashed_pword = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    try:
        db.add(user_sent)
        db.commit()
    except:
        return {"error":"username taken"}
    return {"ok":"user created"}

@router.post("/login")
async def login(user:User_model, db: Session = Depends(get_db)):
    user_vals = db.query(User).filter(User.username==user.username).first()
    if user_vals is None:
        return {"error":"invalid username"}
    if bcrypt.checkpw(user.password.encode(), user_vals.hashed_pword):
        content = {"okay":"signed in"}
        response = JSONResponse(content=content)
        response.set_cookie(key="username", value=user.username)
        return response
    else:
        return {"error":"incorrect password"}

@router.get("/test")
async def testing(username: str = Cookie(None)):
    return {"username":username}

@router.get('/cookie_tester')
async def test_cookie(request: Request):
    return templates.TemplateResponse("tst.html", {"request":request})

@router.post("/cookie")
async def create_cookie():
    content = {"ok":"okay"}
    response = JSONResponse(content=content)
    response.set_cookie(key="username", value="cswil")
    return response
