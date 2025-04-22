# class UserMusicStat(Base):
#     __tablename__ = "UserMusicStat"

#     user_id = Column(Integer, primary_key=True, index=True)
#     top_Listened_Artist = Column(ARRAY(String), nullable=False)
#     top_Listened_Music = Column(ARRAY(String), nullable=False)
#     created_at = Column(TIMESTAMP, server_default=func.now())


from models.userMusicStatModel import UserMusicStat
from sqlalchemy.ext.asyncio import AsyncSession

# async def insert_user_music_stat(db: AsyncSession, music_stat_data: dict):
#     """Insère les statistiques musicales d'un utilisateur dans la base de données."""
#     music_stat = UserMusicStat(
#         user_id= music_stat_data["user_id"],
#         top_Listened_Artist=music_stat_data["top_Listened_Artist"],
#         top_Listened_Music=music_stat_data["top_Listened_Music"],
#     )
#     db.add(music_stat)
#     await db.commit()
#     await db.refresh(music_stat)
#     return music_stat
async def insert_user_music_stat(db: AsyncSession, music_stat_data: dict):
    """Insère les statistiques musicales d'un utilisateur dans la base de données."""

    # Conversion des données complexes vers des listes simples
    artists = [a["artist_name"] for a in music_stat_data.get("top_artists", [])]
    musics = [m["music_name"] for m in music_stat_data.get("top_musics", [])]

    # Création de l’objet UserMusicStat
    music_stat = UserMusicStat(
        user_id=int(music_stat_data["user_id"]),
        top_Listened_Artist=artists,
        top_Listened_Music=musics,
    )

    db.add(music_stat)
    await db.commit()
    await db.refresh(music_stat)
    return music_stat


async def delete_user_music_stat(db: AsyncSession, user_id: int):
    """Supprime les statistiques musicales d'un utilisateur de la base de données."""
    music_stat = await db.get(UserMusicStat, user_id)
    if music_stat:
        await db.delete(music_stat)
        await db.commit()
        return True
    return False

async def update_user_music_stat(db: AsyncSession, user_id: int, music_stat_data: dict):
    """Met à jour les statistiques musicales d'un utilisateur dans la base de données."""
    music_stat = await db.get(UserMusicStat, user_id)
    if music_stat:
        for key, value in music_stat_data.items():
            setattr(music_stat, key, value)
        await db.commit()
        await db.refresh(music_stat)
        return music_stat
    return None



