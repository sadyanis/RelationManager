from sqlalchemy.orm import Session
from models.matchModel import Match
from models.userMusicStatModel import  UserMusicStat
from typing import List

def evaluateCompatibility(userStatistic1: UserMusicStat, userStatistic2: UserMusicStat) -> int:

def getAllPossibleCombination(user_id: int, db: Session) -> List[Match]:

def filterByMusicTaste(matches: List[Match], user_stat: UserMusicStat) -> List[Match]:

def changeStatus(match_id: int, status_code: int, db: Session):

def saveMatch(match: Match, db: Session):

def changeFeedback(match_id: int, user_id: int, score: int, db: Session):