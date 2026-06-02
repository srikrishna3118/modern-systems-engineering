"""
Kafka Pipeline - Event Consumer (Starter Code)

Consumes e-commerce events from Kafka, processes them, and
computes real-time analytics (event counts, revenue tracking).

TODO: Implement the consumer logic.

Run:
  python consumer.py
"""

import json
import signal
import sys
from collections import defaultdict
from datetime import datetime

# pip install kafka-python
# from kafka import KafkaConsumer


class EventAnalytics:
    """Real-time analytics aggregator for e-commerce events."""

    def __init__(self):
        self.event_counts = defaultdict(int)
        self.revenue_by_category = defaultdict(float)
        self.unique_users = set()
        self.total_events = 0
        self.total_revenue = 0.0

    def process_event(self, event: dict):
        """
        TODO: Process an incoming event and update analytics.

        Steps:
        1. Increment total_events
        2. Increment event_counts[event_type]
        3. Add user_id to unique_users set
        4. If event_type is 'purchase':
           - Add total to total_revenue
           - Add total to revenue_by_category[product_category]
        """
        pass

    def get_summary(self) -> str:
        """Return a formatted summary of current analytics."""
        lines = [
            f"\n{'='*50}",
            f"  Real-Time Analytics Summary",
            f"{'='*50}",
            f"  Total Events:    {self.total_events}",
            f"  Unique Users:    {len(self.unique_users)}",
            f"  Total Revenue:   ${self.total_revenue:.2f}",
            f"",
            f"  Events by Type:",
        ]
        for event_type, count in sorted(self.event_counts.items()):
            lines.append(f"    {event_type:20s} {count:>8d}")
        lines.append(f"\n  Revenue by Category:")
        for category, revenue in sorted(self.revenue_by_category.items()):
            lines.append(f"    {category:20s} ${revenue:>10.2f}")
        lines.append(f"{'='*50}")
        return "\n".join(lines)


def create_consumer(topic: str, group_id: str):
    """
    TODO: Create and return a KafkaConsumer instance.

    Configure:
    - bootstrap_servers: 'localhost:9092'
    - group_id: group_id parameter
    - auto_offset_reset: 'earliest' (start from beginning if no committed offset)
    - value_deserializer: JSON deserialization
    - enable_auto_commit: True
    - auto_commit_interval_ms: 5000

    Hint:
        return KafkaConsumer(
            topic,
            bootstrap_servers=['localhost:9092'],
            group_id=group_id,
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            enable_auto_commit=True,
        )
    """
    pass


def main():
    topic = "ecommerce-events"
    group_id = "analytics-group"

    print(f"Starting consumer for topic '{topic}' (group: {group_id})...")
    print("Press Ctrl+C to stop\n")

    analytics = EventAnalytics()

    # TODO: Create the consumer
    # consumer = create_consumer(topic, group_id)

    # Graceful shutdown
    def shutdown(signum, frame):
        print(analytics.get_summary())
        # consumer.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)

    # TODO: Consume messages in a loop
    # for message in consumer:
    #     event = message.value
    #     analytics.process_event(event)
    #
    #     # Print summary every 100 events
    #     if analytics.total_events % 100 == 0:
    #         print(analytics.get_summary())


if __name__ == "__main__":
    main()
