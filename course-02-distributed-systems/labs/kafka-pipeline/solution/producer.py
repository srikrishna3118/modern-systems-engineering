"""
Kafka Pipeline - Event Producer (Solution)

    python producer.py

Stop after N events:

    MAX_EVENTS=50 python producer.py

Choose the partition key with PARTITION_KEY=user_id (default) or product_id.
"""

import json
import os
import time

from kafka import KafkaProducer

from events import generate_event


def create_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=[os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8"),
        acks="all",
        retries=3,
    )


def send_event(producer: KafkaProducer, topic: str, event: dict, key_field: str):
    future = producer.send(topic, key=event[key_field], value=event)
    future.add_errback(lambda exc: print(f"Error sending message: {exc}"))


def main():
    topic = os.environ.get("KAFKA_TOPIC", "ecommerce-events")
    events_per_second = float(os.environ.get("EVENTS_PER_SECOND", "10"))
    max_events = int(os.environ.get("MAX_EVENTS", "0"))
    key_field = os.environ.get("PARTITION_KEY", "user_id")

    print(f"Starting producer for topic '{topic}' (key={key_field})...")
    producer = create_producer()

    count = 0
    try:
        while True:
            event = generate_event()
            send_event(producer, topic, event, key_field)
            count += 1
            if count % 100 == 0:
                print(f"Sent {count} events (latest: {event['event_type']} by {event['user_id']})")
            if max_events and count >= max_events:
                break
            time.sleep(1.0 / events_per_second)
    except KeyboardInterrupt:
        print(f"\nStopped. Total events sent: {count}")
    finally:
        producer.flush()
        producer.close()
        print(f"Flushed {count} events")


if __name__ == "__main__":
    main()
