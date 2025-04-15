from aiokafka import AIOKafkaConsumer
from aiokafka.errors import ConsumerStoppedError
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from Crud.User import insert_user ,delete_user, update_user
from Crud.MusicStat import insert_user_music_stat, delete_user_music_stat, update_user_music_stat
from fastapi import Depends

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"  
KAFKA_TOPICS = [ "user.create","user.update","user.delete","musicStat.create","musicStat.update","musicStat.delete"] # Liste des topics à écouter
KAFKA_GROUP_ID = "relation-manager"  # ID du groupe de consommateurs
KAFKA_AUTO_OFFSET_RESET = "earliest"  # Commencer à lire à partir du début des messages non lus
async def consume_messages():
    """Consomme les messages des topics Kafka."""
    # Crée un consommateur Kafka
    consumer = AIOKafkaConsumer(
        *KAFKA_TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        auto_offset_reset=KAFKA_AUTO_OFFSET_RESET,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))# Désérialisation JSON
    )

    await consumer.start()
    print("Kafka consumer started...")
    try:
        async for msg in consumer:
            topic = msg.topic
            data = msg.value
            async with SessionLocal() as db:
                match topic:
                    case "user.create":
                        await insert_user(db, data)
                    case "user.update":
                        await update_user(db, data["user_id"], data["user_data"])
                    case "user.delete":
                        await delete_user(db, data["user_id"])
                    case "musicStat.create":
                        await insert_user_music_stat(db, data)
                    case "musicStat.update":
                        await update_user_music_stat(db, data["user_id"], data["user_data"])
                    case "musicStat.delete":
                        await delete_user_music_stat(db, data["user_id"])
                # if topic == "user.event":
                #     await handle_user_event(db, data)
                # elif topic == "musicStat.event":
                #     print(f"Message reçu sur le topic {topic}: {data}")
                #     await handle_music_stat_event(db, data)
    finally:
        await consumer.stop()
        print("Kafka consumer stopped.")
        raise ConsumerStoppedError("Kafka consumer stopped unexpectedly.")
                        

# Gestion des événements utilisateur
async def handle_user_event(db: AsyncSession, data: dict):
    match data["event_type"]:
        case "insert":
            await insert_user(db, data["user_data"])
        case "delete":
            await delete_user(db, data["user_id"])
        case "update":
            await update_user(db, data["user_id"], data["user_data"])
            

#Gestion des événements musicStat
async def handle_music_stat_event(db: AsyncSession, data: dict):
    print(f"Event from musicStat: {data}")
    # Exemple : même traitement que user pour l’instant
    match data["event_type"]:
        case "insert":
            await insert_user_music_stat(db, data["user_data"])
        case "delete":
            await delete_user_music_stat(db, data["user_id"])
        case "update":
            await update_user_music_stat(db, data["user_id"], data["user_data"])