from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, index=True)
    is_certified = Column(Integer, nullable=False, default=0)
    is_active = Column(Integer, nullable=False, default=1)
    birthdate = Column(TIMESTAMP, nullable=False)
    gender = Column(String, nullable=False)
    accepted_age_gap = Column(Integer, nullable=False)
    accepted_distance = Column(Integer, nullable=False)
    targeted_gender = Column(String, nullable=False)
    favorite_musician= Column(String, nullable=False)
    favorite_music = Column(String, nullable=False)
    favorite_musical_style = Column(String, nullable=False)
   

    