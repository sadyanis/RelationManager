from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

class Match(Base):
    __tablename__ = "matche"

    match_id= Column(Integer, primary_key=True, index=True, autoincrement=True)
    user1_id = Column(Integer, nullable=False)
    user2_id = Column(Integer, nullable=False)
    match_compatibility = Column(Integer, nullable=False)
    status_code = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())