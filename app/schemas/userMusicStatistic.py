from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserMusicStatisticBase(BaseModel):
    user_id : int
    top_listned_artist : List[str]
    top_listened_music : List[str]

    class Config:
        orm_mode = True

