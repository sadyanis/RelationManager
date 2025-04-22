from aiokafka import AIOKafkaProducer
import json
import logging

logger = logging.getLogger(__name__)

async def get_kafka_producer():
    """Crée et retourne un producteur Kafka"""
    producer = AIOKafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
        logger.info("Kafka producer stopped.")    
    

async def send_kafka_message(producer: AIOKafkaProducer, topic: str, message: dict):
    """Envoie un message à Kafka"""
    try:
        await producer.send_and_wait(topic, message)
        logger.info(f"Message sent to {topic}: {message}")
    except Exception as e:
        logger.error(f"Failed to send message to {topic}: {e}")
        raise