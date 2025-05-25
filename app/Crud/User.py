from models.userModel import User
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import asyncio
async def insert_user(db: AsyncSession, user_data: dict):
    """Insère un utilisateur dans la base de données."""
    if isinstance(user_data.get("birthdate"), str):
        user_data["birthdate"] = datetime.fromisoformat(user_data["birthdate"])
    user = User(
        user_id=user_data["user_id"],
        is_certified=user_data["is_certified"],
        is_active=user_data["is_active"],
        birthdate=user_data["birthdate"],
        gender=user_data["gender"],
        accepted_age_gap=user_data["accepted_age_gap"],
        accepted_distance=user_data["accepted_distance"],
        targeted_gender=user_data["targeted_gender"],
        favorite_musician=user_data["favorite_musician"],
        favorite_music=user_data["favorite_music"],
        favorite_musical_style=user_data["favorite_musical_style"],
    )
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:
        await db.rollback()
        print(f"Erreur lors de l'insertion de l'utilisateur: {e}")
        return None

async def delete_user(db: AsyncSession, user_id: int):
    """Supprime un utilisateur de la base de données."""
    user = await db.get(User, user_id)
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False
async def update_user(db: AsyncSession, user_id: int, user_data: dict):
    """Met à jour un utilisateur dans la base de données."""
    user = await db.get(User, user_id)
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
        return user
    return None