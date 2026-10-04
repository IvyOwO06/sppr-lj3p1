from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)

    scores = relationship(
        "Score",
        back_populates="player",
        cascade="all, delete"
    )

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    player = relationship(
        "Player",
        back_populates="scores"
    )