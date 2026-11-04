"""
In-process stand-in for the Kafka pipeline.

Partitions events the way a key-based Kafka producer would, then runs
one or two consumers in a group over those partitions. Use this to
check the pipeline when Docker is not available. The docker-compose
file in this directory is the real broker path.

    python run_local.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from analytics import EventAnalytics
from events import generate_event


def partition_of(key: str, partitions: int) -> int:
    return sum(key.encode("utf-8")) % partitions


def main():
    partitions = 4
    event_count = int(os.environ.get("MAX_EVENTS", "250"))
    buckets = [[] for _ in range(partitions)]

    for _ in range(event_count):
        event = generate_event()
        buckets[partition_of(event["user_id"], partitions)].append(event)

    # One consumer group member reads every partition: ordering per user holds
    # because a user always lands on the same partition.
    single = EventAnalytics()
    per_user_partitions = {}
    for index, bucket in enumerate(buckets):
        for event in bucket:
            single.process_event(event)
            per_user_partitions.setdefault(event["user_id"], set()).add(index)

    crossed = [uid for uid, parts in per_user_partitions.items() if len(parts) != 1]
    if crossed:
        raise SystemExit(f"user keys crossed partitions: {crossed[:5]}")
    if single.total_events != event_count:
        raise SystemExit("dropped events")

    # Two members of one group: each owns a subset of partitions, and the
    # merged totals match the single consumer.
    group = [EventAnalytics(), EventAnalytics()]
    for index, bucket in enumerate(buckets):
        owner = group[index % len(group)]
        for event in bucket:
            owner.process_event(event)

    merged_events = sum(member.total_events for member in group)
    merged_revenue = sum(member.total_revenue for member in group)
    if merged_events != single.total_events:
        raise SystemExit("consumer group did not cover every event")
    if abs(merged_revenue - single.total_revenue) > 0.001:
        raise SystemExit("revenue diverged across the group")

    print(single.get_summary())
    print(
        f"\nPartition sizes: {[len(bucket) for bucket in buckets]}\n"
        f"Group members processed "
        f"{group[0].total_events} and {group[1].total_events} events."
    )
    print("local pipeline ok")


if __name__ == "__main__":
    main()
