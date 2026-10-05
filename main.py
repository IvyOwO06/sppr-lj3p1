from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routes.players import router as player_router
from routes.scores import router as score_router

import models
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return "Welcome to my python api"

app.include_router(player_router)
app.include_router(score_router)