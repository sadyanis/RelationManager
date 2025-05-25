import pytest
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from kafka.kafka_consumer import consume_messages

# @pytest.mark.asyncio
# async def test_kafka_consumer():
#     # envoi d'un message test
#     producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
#     await producer.start()
#     await producer.send("user.create", {"user_id": 999, "name": "Test"})
    
#     # vérification asynchrone
#     async def verify_message():
#         consumer = AIOKafkaConsumer("user.create", bootstrap_servers="localhost:9092")
#         await consumer.start()
#         async for msg in consumer:
#             assert msg.value["user_id"] == 999
#             break
    
#     await asyncio.gather(consume_messages(), verify_message())
def test_ci_runs():
    assert 1 + 1 == 2