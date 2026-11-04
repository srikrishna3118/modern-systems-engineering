"""
Kafka Pipeline - Event Consumer (Solution)

Consumes e-commerce events and prints a running analytics summary.

Run against a broker (see docker-compose.yml):

    python consumer.py

Stop after N events (useful for a smoke test):

    MAX_EVENTS=100 python consumer.py
"""

import json
import os
import signal
import sys

from kafka import KafkaConsumer

from analytics import EventAnalytics


def create_consumer(topic: str, group_id: str) -> KafkaConsumer:
    return KafkaConsumer(
        topic,
        bootstrap_servers=[os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")],
        group_id=group_id,
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        enable_auto_commit=True,
        auto_commit_interval_ms=5000,
    )


def main():
    topic = os.environ.get("KAFKA_TOPIC", "ecommerce-events")
    group_id = os.environ.get("KAFKA_GROUP", "analytics-group")
    max_events = int(os.environ.get("MAX_EVENTS", "0"))

    print(f"Starting consumer for topic '{topic}' (group: {group_id})...")
    analytics = EventAnalytics()
    consumer = create_consumer(topic, group_id)

    def shutdown(signum, frame):
        print(analytics.get_summary())
        consumer.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)

    for message in consumer:
        analytics.process_event(message.value)
        if analytics.total_events % 100 == 0:
            print(analytics.get_summary())
        if max_events and analytics.total_events >= max_events:
            print(analytics.get_summary())
            consumer.close()
            return


if __name__ == "__main__":
    main()
