from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.feedbackModel import Feedback
from models.matchModel import Match
from models.userMusicStatModel import  UserMusicStat
from models.userModel import User
from models.enums import MatchStatus
from typing import List

#def evaluateCompatibility(userStatistic1: UserMusicStat, userStatistic2: UserMusicStat) -> int:

#def getAllPossibleCombination(user_id: int, db: Session) -> List[Match]:

#def filterByMusicTaste(matches: List[Match], user_stat: UserMusicStat) -> List[Match]:

async def changeStatus(match: Match, user: User, hasMatch: bool, db: AsyncSession):
    """Change le statut d'un match dans la base de données"""
    if hasMatch:
        if match.status_code in {MatchStatus.MATCH_USER1, MatchStatus.MATCH_USER2}:
            match.status_code = MatchStatus.MATCH
        else:
            match.status_code = (
                MatchStatus.MATCH_USER1 if match.user1_id == user.user_id else MatchStatus.MATCH_USER2
            )
    else:
        match.status_code = MatchStatus.NOT_MATCH

    await db.commit()
    await db.refresh(match)
    return match


async def saveMatch(match: Match, db: AsyncSession):
    """Enregistre un match dans la base de données"""
    await db.add(match)
    await db.commit()
    await db.refresh(match)
    return match
    
async def changeFeedback(match:Match, user:User, score: int, db:AsyncSession):
    """met à jour le retour d'un utilisateur sur un match"""
    feedback = await db.execute(
        select(Feedback).where(Feedback.match_id == match.match_id)
    )
    feedback = feedback.scalars().first()
    if feedback.user1_id == user.user_id:
        feedback.user1_score = score
    else:
        feedback.user2_score = score
    await db.commit()
    await db.refresh(feedback)
      
async def saveMatches(matches: List[Match], db: AsyncSession):
    """Enregistre une liste de match dans la base de données"""
    for match in matches:
        await db.add(match)
    await db.commit()
    return matches
 
#async def updateUserInformation(user:User):