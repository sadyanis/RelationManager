from sentence_transformers import util, SentenceTransformer
from sqlalchemy.orm import Session
from models.userModel import User
from models.userMusicStatModel import UserMusicStat
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import numpy as np

class MusicMatchEngine:
    def __init__(self, model):
        self.model = model
    async def get_users_id(self, db: AsyncSession , id: int) -> List[int]:
        """Récupère tous les IDs d'utilisateurs depuis la base de données"""
        result = await db.execute(select(User.user_id).where(User.user_id != id))
        users = result.scalars().all()
        return users
    async def get_user_data(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """Récupère les données utilisateur depuis la base de données"""
        result_user = await db.execute(
        select(User).where(User.user_id == user_id)
    )
        user = result_user.scalars().first()
        if not user:
            return None
        # Récupérer les statistiques musicales de l'utilisateur
        stats_result = await db.execute(
            select(UserMusicStat).where(UserMusicStat.user_id == user_id)
        )
        stats = stats_result.scalars().first()
        # Convertir les résultats en dictionnaire
        
        return {
            'user_id': user.user_id,
            'gender': user.gender,
            'targeted_gender': user.targeted_gender,
            'birthdate': user.birthdate.isoformat(),
            'accepted_age_gap': user.accepted_age_gap,
            'favorite_musical_style': user.favorite_musical_style,
            'top_Listened_Artist': stats.top_Listened_Artist if stats else [],
            'top_Listened_Music': stats.top_Listened_Music if stats else []
        }

    def preprocess_profile(self, user: dict) -> str:
        """Convertit un profil utilisateur en texte pour l'embedding"""
        return f"""
        Genre: {user['gender']} | Target: {user['targeted_gender']}
        Age: {user['birthdate'][:4]} | AgeGap: {user['accepted_age_gap']}
        Style: {user['favorite_musical_style']}
        Artists: {' '.join(user['top_Listened_Artist'])}
        Tracks: {' '.join(user['top_Listened_Music'])}
        """

    async def calculate_compatibility(self, user1: dict, user2: dict) -> dict:
        # 1. Vérification des critères de base
        age1 = int(user1['birthdate'][:4])
        age2 = int(user2['birthdate'][:4])
        age_gap = abs(age1 - age2)

        if age_gap > min(user1['accepted_age_gap'], user2['accepted_age_gap']):
            return {"user1":user1['user_id'] ,"user2":user2['user_id'],"match_percentage": 0, "reason": "Écart d'âge trop important"}

        if not (user1['gender'] in user2['targeted_gender'] and 
                user2['gender'] in user1['targeted_gender']):
            return {"user1":user1['user_id'] ,"user2":user2['user_id'],  "match_percentage": 0, "reason": "Incompatibilité de genre"}

        # 2. Calcul de la similarité musicale
        text1 = self.preprocess_profile(user1)
        text2 = self.preprocess_profile(user2)
        
        emb1 = self.model.encode(text1, convert_to_tensor=True)
        emb2 = self.model.encode(text2, convert_to_tensor=True)
        
        music_similarity = util.cos_sim(emb1, emb2).item()

        # 3. Score composite (ajustez les poids selon vos besoins)
        match_percentage = int((music_similarity * 0.7 + 0.2) * 100)  # Garantit un minimum de 30%

        return {
            "user1": user1['user_id'],
            "user2": user2['user_id'],
            "match_percentage": min(match_percentage, 100),  # Max 100%
            "age_compatibility": f"{age_gap} ans (toléré: {user1['accepted_age_gap']}/{user2['accepted_age_gap']})",
            "music_similarity": f"{music_similarity:.2f}",
            "top_common_artists": self._find_common_artists(user1, user2)
        }

    def _find_common_artists(self, user1: dict, user2: dict) -> list:
        """Trouve des artistes similaires (même partiellement)"""
        from difflib import get_close_matches
        common = []
        for artist in user1['top_Listened_Artist']:
            matches = get_close_matches(artist, user2['top_Listened_Artist'], cutoff=0.6)
            common.extend(matches)
        return list(set(common))