from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.feedbackModel import Feedback
from models.matchModel import Match
from models.userMusicStatModel import  UserMusicStat
from models.userModel import User
from models.enums import MatchStatus
from typing import List
from schemas.User import UserBase
from sentence_transformers import SentenceTransformer
from matching import MusicMatchEngine
from aiokafka import AIOKafkaProducer
import json
import os


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


async def saveMatch(match: Match, db: AsyncSession , kafka_producer: AIOKafkaProducer = None):
    """Enregistre un match dans la base de données"""
    # d'abord verifier si ce match existe dans la base de données
    existing_match = await db.execute(
        select(Match).where(
            (Match.user1_id == match.user1_id) & (Match.user2_id == match.user2_id)
        )
    )
    existing_match = existing_match.scalars().first()
    if existing_match:
        # Si le match existe déjà, on le met à jour
        
        return existing_match
    
    db.add(match)
    try:
        await db.commit()
        await db.refresh(match)
    except Exception as e:
        await db.rollback()
        print(f"Erreur lors de l'enregistrement du match: {e}")
        raise e
    if kafka_producer:
        event = {
            "match_id": match.match_id,
            "user1_id": match.user1_id,
            "user2_id": match.user2_id,
            "match_compatiblity": match.match_compatiblity,
            "status_code": match.status_code
        }
        
        try:
            await kafka_producer.send_and_wait(
                topic="matche.create",
                value=event
            )
        except Exception as e:
            print(f"Erreur d'envoi Kafka: {e}")
    return match
    
async def changeFeedback(match:int, user:int, score: int, db:AsyncSession):
    """met à jour le retour d'un utilisateur sur un match"""
    feedback = await getFeedBack(match, db)
    if feedback.user1_id == user:
        feedback.score_user1 = score
    elif feedback.user2_id == user:
        feedback.score_user2 = score
    else:
        raise ValueError("L'utilisateur ne correspond pas au match")
    await db.commit()
    await db.refresh(feedback)
    return feedback
      
async def saveMatches(matches: List[Match], db: AsyncSession):
    """Enregistre une liste de match dans la base de données"""
    for match in matches:
        await db.add(match)
    await db.commit()
    return matches
 
#async def updateUserInformation(user:User):
#async def evaluateCompatibility(user1: User, user2: User, db: AsyncSession) -> int:
# Calcule et enregistre les matches d'un utilisateur
async def getMatches(
    user_id: int, 
    db: AsyncSession,
    match_engine: MusicMatchEngine,
    kafka_producer: AIOKafkaProducer

):
    user = await match_engine.get_user_data(db, user_id)
    users_ids = await match_engine.get_users_id(db, user_id)
    
    results = []

    for other_user_id in users_ids:
        other_user = await match_engine.get_user_data(db, other_user_id)
        result = await match_engine.calculate_compatibility(user, other_user)
        match = getMatchfromDict(result)
        await saveMatch(match, db,kafka_producer )
        results.append(result)
    
    return results

def getMatchfromDict(match: dict) -> Match:
    """Convertit un dictionnaire de match en objet Match"""
    return Match(
        user1_id=match["user1"],
        user2_id=match["user2"],
        match_compatiblity=match["match_percentage"],
        status_code=match["status_code"]
    )

async def getFeedBack(
    match: int,
    db: AsyncSession
) -> Feedback:
    """Récupère le feedback d'un match"""
    feedback = await db.execute(
        select(Feedback).where(Feedback.match_id == match)
    )
    return feedback.scalars().first() if feedback else None

async def updateUserInformation(user_data: UserBase, db: AsyncSession):
    result = await db.execute(select(User).where(User.user_id == user_data.user_id))
    user = result.scalars().first()
    if not user:
        raise ValueError("Utilisateur non trouvé")
    user.is_certified = user_data.is_certified
    user.is_active = user_data.is_active
    user.birthdate = user_data.birthdate
    user.gender = user_data.gender
    user.accepted_age_gap = user_data.accepted_age_gap
    user.accepted_distance = user_data.accepted_distance
    user.targeted_gender = user_data.targeted_gender
    user.favorite_musician = user_data.favorite_musician
    user.favorite_music = user_data.favorite_music
    user.favorite_musical_style = user_data.favorite_musical_style
    
    

    await db.commit()
    await db.refresh(user)
    return user

async def deleteMatch(
    match_id: int,
    db: AsyncSession
) -> Match:
    """Supprime un match"""
    match = await db.execute(select(Match).where(Match.match_id == match_id))
    match = match.scalars().first()
    if not match:
        raise ValueError("Match non trouvé")
    
    await db.delete(match)
    await db.commit()
    return match
    
async def CheckExistingMatch(
    user1_id: int,
    user2_id: int,
    db: AsyncSession
) -> Match:
    """Vérifie si un match existe déjà"""
    match = await db.execute(
        select(Match).where(
            (Match.user1_id == user1_id) & (Match.user2_id == user2_id)
        )
    )
    return True if match else False