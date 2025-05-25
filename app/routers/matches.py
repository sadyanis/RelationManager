from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, HTTPException
from schemas.UserInput  import UserInput, MatchRequest
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer
from matching import MusicMatchEngine
from sqlalchemy.orm import Session
from database import get_db  

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/{id_user}")
async def match(user_id: int, db: AsyncSession = Depends(get_db)):
    if not hasattr(app.state, 'match_engine'):
        raise HTTPException(
            status_code=503,
            detail="Service non prêt: moteur de matching non chargé"
        )
    # Appel de la méthode de matching
    user = await app.state.match_engine.get_user_data(db,user_id)
    users = await app.state.match_engine.get_users_id(db,user_id)
    results = []
    user1 = await app.state.match_engine.get_user_data(db,user_id)
    for user2 in users:
        user2 = await app.state.match_engine.get_user_data(db,user2)
        result = await app.state.match_engine.calculate_compatibility(user1, user2)
        results.append(result)
    return results