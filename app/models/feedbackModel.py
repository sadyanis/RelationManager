from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    match_id= Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, nullable=False)
    user2_id = Column(Integer, nullable=False)
    score_user1 = Column(Integer, nullable=True)
    score_user2 = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


    