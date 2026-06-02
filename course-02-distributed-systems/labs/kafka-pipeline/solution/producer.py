"""
Kafka Pipeline - Event Producer (Solution)
"""

import json
import time
import random
import uuid
from datetime import datetime

from kafka import KafkaProducer

EVENT_TYPES = ["page_view", "add_to_cart", "remove_from_cart", "purchase", "search"]
PRODUCTS = [
    {"id": "P001", "name": "Wireless Headphones", "price": 79.99, "category": "electronics"},
    {"id": "P002", "name": "Running Shoes", "price": 129.99, "category": "sports"},
    {"id": "P003", "name": "Python Cookbook", "price": 49.99, "category": "books"},
    {"id": "P004", "name": "Mechanical Keyboard", "price": 149.99, "category": "electronics"},
    {"id": "P005", "name": "Coffee Maker", "price": 89.99, "category": "kitchen"},
]
USER_IDS = [f"user_{i:04d}" for i in range(1, 101)]


def generate_event() -> dict:
    event_type = random.choice(EVENT_TYPES)
    user_id = random.choice(USER_IDS)
    product = random.choice(PRODUCTS)

    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_id,
        "product_id": product["id"],
        "product_name": product["name"],
        "product_category": product["category"],
        "price": product["price"],
    }

    if event_type == "search":
        event["query"] = random.choice(["headphones", "shoes", "books", "keyboard", "coffee"])
    if event_type == "purchase":
        event["quantity"] = random.randint(1, 3)
        event["total"] = event["price"] * event["quantity"]

    return event


def create_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8"),
        acks="all",
        retries=3,
    )


def on_send_success(record_metadata):
    pass  # Optionally log: topic, partition, offset


def on_send_error(excp):
    print(f"Error sending message: {excp}")


def send_event(producer: KafkaProducer, topic: str, event: dict):
    future = producer.send(topic, key=event["user_id"], value=event)
    future.add_callback(on_send_success).add_errback(on_send_error)


def main():
    topic = "ecommerce-events"
    events_per_second = 10

    print(f"Starting producer for topic '{topic}'...")
    producer = create_producer()

    try:
        count = 0
        while True:
            event = generate_event()
            send_event(producer, topic, event)
            count += 1
            if count % 100 == 0:
                print(f"Sent {count} events (latest: {event['event_type']} by {event['user_id']})")
            time.sleep(1.0 / events_per_second)
    except KeyboardInterrupt:
        print(f"\nStopped. Total events sent: {count}")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()
