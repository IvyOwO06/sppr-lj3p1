from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import models
from database import SessionLocal
from schemas import Score

router = APIRouter(
    tags={"Scores"}
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close

@router.post("/players/{id}/scores")
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

@router.get("/players/{id}/scores")
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

@router.delete("/scores/{id}")
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