import uvicorn
from fastapi import FastAPI
from endpoints import hello_world

app = FastAPI()

app.include_router(
    hello_world.router,
    responses={404:{"description":"not found"}}
)

uvicorn.run(app)