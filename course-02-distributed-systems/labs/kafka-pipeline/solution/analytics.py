"""Real-time analytics aggregator for e-commerce events.

Shared by the Kafka consumer and the in-process demo so the
aggregation can be checked without a broker.
"""

from collections import defaultdict


class EventAnalytics:
    """Fold a stream of events into counts, uniques, and revenue."""

    def __init__(self):
        self.event_counts = defaultdict(int)
        self.revenue_by_category = defaultdict(float)
        self.unique_users = set()
        self.total_events = 0
        self.total_revenue = 0.0

    def process_event(self, event: dict):
        self.total_events += 1
        event_type = event.get("event_type", "unknown")
        self.event_counts[event_type] += 1
        user_id = event.get("user_id")
        if user_id:
            self.unique_users.add(user_id)
        if event_type == "purchase":
            total = float(event.get("total") or 0)
            self.total_revenue += total
            category = event.get("product_category", "unknown")
            self.revenue_by_category[category] += total

    def get_summary(self) -> str:
        lines = [
            f"\n{'=' * 50}",
            "  Real-Time Analytics Summary",
            f"{'=' * 50}",
            f"  Total Events:    {self.total_events}",
            f"  Unique Users:    {len(self.unique_users)}",
            f"  Total Revenue:   ${self.total_revenue:.2f}",
            "",
            "  Events by Type:",
        ]
        for event_type, count in sorted(self.event_counts.items()):
            lines.append(f"    {event_type:20s} {count:>8d}")
        lines.append("\n  Revenue by Category:")
        for category, revenue in sorted(self.revenue_by_category.items()):
            lines.append(f"    {category:20s} ${revenue:>10.2f}")
        lines.append(f"{'=' * 50}")
        return "\n".join(lines)
