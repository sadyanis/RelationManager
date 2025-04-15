from pydantic import BaseModel
from datetime import datetime

class UserInput(BaseModel):
    user_id: int
    birthdate: datetime
    gender: str
    targeted_gender: str
    accepted_age_gap: int
    favorite_musician: list[str]
    favorite_music: list[str]
    favorite_musical_style: str

class MatchRequest(BaseModel):
    user1: UserInput
    user2: UserInput
     
