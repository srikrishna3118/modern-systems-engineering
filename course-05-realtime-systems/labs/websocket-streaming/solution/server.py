"""
WebSocket real-time streaming server (solution).

Pub/sub by stock symbol, with a bounded per-client queue so a slow
subscriber cannot stall the producer or other clients.

    pip install -r requirements.txt
    python server.py
"""

import asyncio
import json
import logging
import os
import random
from datetime import datetime, timezone

import websockets

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

STOCKS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "NVDA"]
STOCK_PRICES = {stock: 100 + random.randint(-50, 50) for stock in STOCKS}


class RealTimeServer:
    """Tracks channel membership and a bounded outbound queue per socket."""

    def __init__(self, max_backlog: int = 100):
        self._subscribers = {}  # channel -> set[websocket]
        self._queues = {}  # websocket -> asyncio.Queue
        self._channels = {}  # websocket -> set[str]
        self._max_backlog = max_backlog
        self.dropped = 0

    def subscribe(self, websocket, channel: str):
        self._subscribers.setdefault(channel, set()).add(websocket)
        self._channels.setdefault(websocket, set()).add(channel)
        self._queues.setdefault(websocket, asyncio.Queue(maxsize=self._max_backlog))
        logger.info(
            "Client subscribed to %s (total: %d)",
            channel,
            len(self._subscribers[channel]),
        )

    def unsubscribe(self, websocket, channel: str):
        members = self._subscribers.get(channel)
        if members is not None:
            members.discard(websocket)
            if not members:
                del self._subscribers[channel]
        if websocket in self._channels:
            self._channels[websocket].discard(channel)
        logger.info("Client unsubscribed from %s", channel)

    def disconnect(self, websocket):
        for channel in list(self._channels.get(websocket, ())):
            self.unsubscribe(websocket, channel)
        self._channels.pop(websocket, None)
        self._queues.pop(websocket, None)

    def publish(self, channel: str, message: dict) -> int:
        """Enqueue to each subscriber. A full queue drops that message for that client."""
        payload = json.dumps(message)
        delivered = 0
        for websocket in list(self._subscribers.get(channel, ())):
            queue = self._queues.get(websocket)
            if queue is None:
                continue
            try:
                queue.put_nowait(payload)
                delivered += 1
            except asyncio.QueueFull:
                self.dropped += 1
                logger.warning("Dropping update for a slow subscriber on %s", channel)
        return delivered

    async def writer(self, websocket):
        queue = self._queues.setdefault(websocket, asyncio.Queue(maxsize=self._max_backlog))
        try:
            while True:
                payload = await queue.get()
                await websocket.send(payload)
        except websockets.exceptions.ConnectionClosed:
            pass

    async def handle_client(self, websocket, *args):
        writer_task = asyncio.create_task(self.writer(websocket))
        try:
            async for raw in websocket:
                data = json.loads(raw)
                action = data.get("action")
                channel = data.get("channel")
                if not channel:
                    continue
                if action == "subscribe":
                    self.subscribe(websocket, channel)
                elif action == "unsubscribe":
                    self.unsubscribe(websocket, channel)
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as exc:
            logger.error("Client error: %s", exc)
        finally:
            writer_task.cancel()
            self.disconnect(websocket)
            logger.info("Client disconnected")


async def data_producer(server: RealTimeServer, interval: float = 0.5):
    while True:
        stock = random.choice(STOCKS)
        change = random.uniform(-0.01, 0.01)
        STOCK_PRICES[stock] *= 1 + change
        server.publish(
            stock,
            {
                "stock": stock,
                "price": round(STOCK_PRICES[stock], 2),
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            },
        )
        await asyncio.sleep(interval)


async def main():
    server = RealTimeServer()
    host = os.environ.get("BIND_HOST", "localhost")
    port = int(os.environ.get("PORT", "8765"))
    async with websockets.serve(server.handle_client, host, port):
        logger.info("WebSocket server started on ws://%s:%s", host, port)
        producer_task = asyncio.create_task(data_producer(server))
        try:
            await asyncio.Future()
        finally:
            producer_task.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
