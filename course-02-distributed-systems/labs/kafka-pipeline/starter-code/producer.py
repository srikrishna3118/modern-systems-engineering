"""
Kafka Pipeline - Event Producer (Starter Code)

Produces simulated e-commerce events (page views, add-to-cart, purchases)
to a Kafka topic.

TODO: Implement the producer logic to send events to Kafka.

Run:
  docker-compose up -d
  pip install -r requirements.txt
  python producer.py
"""

import json
import time
import random
import uuid
from datetime import datetime

# pip install kafka-python
# from kafka import KafkaProducer

# Event types and sample data
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
    """Generate a random e-commerce event."""
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


def create_producer():
    """
    TODO: Create and return a KafkaProducer instance.

    Configure:
    - bootstrap_servers: 'localhost:9092'
    - value_serializer: JSON serialization (json.dumps + encode to utf-8)
    - key_serializer: string encoding (str.encode)
    - acks: 'all' (wait for all replicas)
    - retries: 3

    Hint:
        return KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8'),
            acks='all',
            retries=3,
        )
    """
    pass


def send_event(producer, topic: str, event: dict):
    """
    TODO: Send an event to Kafka.

    Use the user_id as the partition key to ensure all events
    from the same user go to the same partition (ordering guarantee).

    Steps:
    1. Call producer.send(topic, key=event['user_id'], value=event)
    2. Optionally add a callback for success/error logging
    """
    pass


def main():
    topic = "ecommerce-events"
    events_per_second = 10

    print(f"Starting producer for topic '{topic}'...")
    print(f"Generating ~{events_per_second} events/second")
    print("Press Ctrl+C to stop\n")

    # TODO: Create the producer
    # producer = create_producer()

    try:
        count = 0
        while True:
            event = generate_event()

            # TODO: Send the event
            # send_event(producer, topic, event)

            count += 1
            if count % 100 == 0:
                print(f"Sent {count} events")

            time.sleep(1.0 / events_per_second)

    except KeyboardInterrupt:
        print(f"\nStopped. Total events sent: {count}")
    finally:
        # TODO: Flush and close the producer
        # producer.flush()
        # producer.close()
        pass


if __name__ == "__main__":
    main()
