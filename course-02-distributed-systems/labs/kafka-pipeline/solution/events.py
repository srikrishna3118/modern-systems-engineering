"""E-commerce event generator shared by the Kafka producer and the local demo."""

import random
import uuid
from datetime import datetime, timezone

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
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
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
        event["total"] = round(event["price"] * event["quantity"], 2)

    return event
