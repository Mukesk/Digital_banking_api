import pika
import json
from app.core.config import settings
import logging

def publish_event(event_name: str, payload: dict):
    try:
        connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
        channel = connection.channel()
        channel.exchange_declare(exchange='banking', exchange_type='topic')
        
        # Serialize datetime effectively
        payload_str = json.dumps(payload, default=str)
        
        channel.basic_publish(
            exchange='banking',
            routing_key=event_name,
            body=payload_str
        )
        connection.close()
    except Exception as e:
        # In production use persistent retry queues
        logging.error(f"Failed to publish event {event_name}: {e}")
