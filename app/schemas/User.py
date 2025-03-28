from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    user_id: int
    is_certified: bool
    is_active: bool
    birthdate: datetime
    gender: str
    accepted_age_gap: int
    accepted_distance: int
    targeted_gender: str
    favorite_musician: str
    favorite_music: str
    favorite_musical_style: str

    class Config:
        orm_mode = True