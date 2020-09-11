import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from endpoints import hello_world

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    hello_world.router,
    responses={404: {"description": "not found"}}
)

uvicorn.run(app)
