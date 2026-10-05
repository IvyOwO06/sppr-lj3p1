from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import models
from database import SessionLocal
from schemas import PlayerCreate, PlayerEdit

router = APIRouter(
    prefix="/players",
    tags=["Players"]
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.get("")
def get_players(db: Session = Depends(get_db)):
    return db.query(models.Player).all()

@router.get("/{id}")
def get_player(
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
    
    return player

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    players = db.query(models.Player).all()

    players.sort(
        key=lambda player: player.scores[-1].scoere if player.scores else 0,
        reverse=True
    )

    return players

@router.post("/add")
def create_player(
    player_data: PlayerCreate,
    db: Session = Depends(get_db)
):
    new_player = models.Player(
        username=player_data.username
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return new_player

@router.patch("/edit/{id}")
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

    player.username = edited_player.usernmame

    db.commit()
    db.refresh(player)

    return player

@router.delete("/{id}")
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