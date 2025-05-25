from aiokafka import AIOKafkaProducer
import asyncio
import json
from datetime import datetime

async def send_test_message():
    producer = AIOKafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()

    test_data = {
        "user.create": {"user_id": 180, "is_certified": 1,
            "is_active": 1,
            "birthdate": "1995-06-15T00:00:00",
            "gender": "male",
            "accepted_age_gap": 5,
            "accepted_distance": 50,
            "targeted_gender": "F",
            "favorite_musician": "Ed Sheeran",
            "favorite_music": "Perfect",
            "favorite_musical_style": "pop"},
        "user.delete": {"user_id": 2},
        "user.update": {"user_id": 19, "is_certified": 1,
            "is_active": 0,
            },
    }

    for topic, message in test_data.items():
        await producer.send(topic, message)
        print(f"Message envoyé sur {topic}: {message}")

    await producer.stop()

asyncio.run(send_test_message())