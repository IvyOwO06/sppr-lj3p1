from pydantic import BaseModel, Field

class PlayerCreate(BaseModel):
    username: str = Field(min_length=1)

class PlayerEdit(BaseModel):
    username: str = Field(min_length=1)

class Score(BaseModel):
    score: int = Field(gt=0)