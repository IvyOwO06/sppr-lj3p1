from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
import models

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# class Player(BaseModel):
#     id: int = Field(gt=0)
#     username: str = Field(min_length=1)
#     score: int = Field(ge=0)

class PlayerCreate(BaseModel):
    username: str = Field(min_length=1)

class Score(BaseModel):
    score: int = Field(gt=0)

class PlayerEdit(BaseModel):
    username: str = Field(min_length=1)

@app.get("/")
def root():
    return "Welcome to the Python api"

@app.get("/players")
def get_players(db: Session = Depends(get_db)):
    return db.query(models.Player).all()


@app.get("/players/{id}")
def get_player(id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(
        models.Player.id == id
    ).first()

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    return player


@app.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    players = db.query(models.Player).all()

    players.sort(
        key=lambda player: player.scores[-1].score if player.scores else 0,
        reverse=True
    )

    return players

@app.post("/players/add")
def create_player(player_data: PlayerCreate, db: Session = Depends(get_db)):
    new_player = models.Player(
        username=player_data.username
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return new_player

@app.patch("/players/edit/{id}")
def edit_player(
    id: int,
    edited_player: PlayerEdit,
    db: Session = Depends(get_db)
):
    player = db.query(models.Player).filter(
        models.Player.id == id
    ).first()

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    player.username = edited_player.username

    db.commit()
    db.refresh(player)

    return player

@app.post("/players/{id}/scores")
def add_score(
    id: int,
    score_data: Score,
    db: Session = Depends(get_db)
):
    player = db.query(models.Player).filter(
        models.Player.id == id
    ).first()

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    new_score = models.Score(
        score=score_data.score,
        player_id=id
    )

    db.add(new_score)
    db.commit()
    db.refresh(new_score)

    return new_score

@app.delete("/players/{id}")
def delete_player(
    id: int,
    db: Session = Depends(get_db)
):
    player = db.query(models.Player).filter(
        models.Player.id == id
    ).first()

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    db.delete(player)
    db.commit()

    return f"Player with id {id} deleted"

@app.delete("/scores/{id}")
def delete_score(
    id: int,
    db: Session = Depends(get_db)
):
    score = db.query(models.Score).filter(
        models.Score.id == id
    ).first()

    if score is None:
        raise HTTPException(
            status_code=404,
            detail="Score not found"
        )

    db.delete(score)
    db.commit()

    return f"Score with id {id} deleted"

@app.get("/players/{id}/scores")
def get_scores(
    id: int,
    db: Session = Depends(get_db)
):
    player = db.query(models.Player).filter(
        models.Player.id == id
    ).first()

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    return player.scores