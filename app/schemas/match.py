from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from models.enums import MatchStatusCode

class MatchBase(BaseModel):
    user1_id : int
    user2_id : int
    match_compatiblity : int
    status_code : MatchStatusCode

class MatchCreate(MatchBase):
    pass

class MatchResponse(MatchBase):
    id : int
    created_at : datetime
    
    class Config:
        orm_mode = True