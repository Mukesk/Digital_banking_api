import pika
import json
import threading
import logging
from app.core.config import settings

# In-memory storage for reporting simplified for this exercise.
# A proper implementation would use a database.
stats = {
    "total_accounts": 0,
    "total_loans": 0,
    "total_transactions_today": 0,
    "total_amount_transferred_today": 0.0
}

def update_stats(data: dict):
    # This expects event data. Depending on 'type' or routing key, we could know if it's a loan or a transaction.
    # We will infer it based on fields.
    if 'transaction_id' in data:
        stats["total_transactions_today"] += 1
        stats["total_amount_transferred_today"] += data.get("amount", 0.0)
    elif 'loan_id' in data:
        stats["total_loans"] += 1
        
    logging.info(f"Updated stats: {stats}")

def start_consumer():
    try:
        connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
        channel = connection.channel()
        channel.exchange_declare(exchange='banking', exchange_type='topic')
        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        
        channel.queue_bind(queue_name, 'banking', 'transaction.completed')
        channel.queue_bind(queue_name, 'banking', 'loan.approved')

        def callback(ch, method, properties, body):
            data = json.loads(body)
            update_stats(data)

        channel.basic_consume(queue_name, callback, auto_ack=True)
        logging.info("Started RabbitMQ consumer in Reporting Service...")
        channel.start_consuming()
    except Exception as e:
        logging.error(f"Error starting consumer: {e}")

def run_consumer_in_background():
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start()
