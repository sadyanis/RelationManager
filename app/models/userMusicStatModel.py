from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

class UserMusicStat(Base):
    __tablename__ = "UserMusicStat"

    user_id = Column(Integer, primary_key=True, index=True)
    top_Listened_Artist = Column(ARRAY(String), nullable=False)
    top_Listened_Music = Column(ARRAY(String), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())