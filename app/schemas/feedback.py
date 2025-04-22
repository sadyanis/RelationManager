from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FeedbackBase(BaseModel):
    match_id : int
    user1_id : int
    user2_id : int
    score_user1 : Optional[int]
    score_user2 : Optional[int]

class FeedbackCreate(BaseModel):
    match_id : int
    user_id : int
    score : int

class FeedbackResponse(FeedbackBase):
    created_at : datetime

    class Config:
        orm_mode = True