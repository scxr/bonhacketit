import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from endpoints import index_router, create_new_recipe, auth_router, recipe_interact_router
from db.base import engine
from models import db_models

db_models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    index_router.router,
    responses={404: {"description": "not found"}}
)

app.include_router(
    create_new_recipe.router,
    responses={404: {"description": "not found"}}
)

app.include_router(
    auth_router.router,
    responses={404: {"description": "not found"}}
)

app.include_router(
    recipe_interact_router.router,
    responses={404: {"description": "not found"}}
)


uvicorn.run(app)
