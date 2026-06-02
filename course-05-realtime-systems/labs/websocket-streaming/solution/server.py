"""
WebSocket Real-Time Streaming Server (Solution)

Complete implementation with pub/sub pattern and backpressure handling.
"""

import asyncio
import json
import logging
import random
from datetime import datetime
from collections import defaultdict

import websockets

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# Stock data
STOCKS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "NVDA"]
STOCK_PRICES = {stock: 100 + random.randint(-50, 50) for stock in STOCKS}


class RealTimeServer:
    """WebSocket server for real-time data streaming with pub/sub pattern."""

    def __init__(self):
        self._subscribers = defaultdict(set)  # channel -> {websocket}
        self._buffer_sizes = {}  # websocket -> current buffer size

    async def subscribe(self, websocket, channel: str):
        """Add a client to the subscribers set for a channel."""
        self._subscribers[channel].add(websocket)
        self._buffer_sizes[websocket] = 0
        logger.info(f"Client subscribed to {channel} (total: {len(self._subscribers[channel])})")

    async def unsubscribe(self, websocket, channel: str):
        """Remove a client from a channel's subscribers."""
        self._subscribers[channel].discard(websocket)
        if not self._subscribers[channel]:
            del self._subscribers[channel]
        if websocket in self._buffer_sizes:
            del self._buffer_sizes[websocket]
        logger.info(f"Client unsubscribed from {channel}")

    async def broadcast(self, channel: str, message: dict, max_backlog: int = 100):
        """Broadcast a message to all subscribers on a channel with backpressure handling."""
        if channel not in self._subscribers:
            return

        disconnected = []
        
        for websocket in list(self._subscribers[channel]):
            try:
                self._buffer_sizes[websocket] += 1
                
                # Check for backpressure (slow subscriber)
                if self._buffer_sizes[websocket] > max_backlog:
                    logger.warning(f"Backlog exceeded for a client; disconnecting")
                    disconnected.append(websocket)
                    continue

                # Send the message
                await websocket.send(json.dumps(message))
                self._buffer_sizes[websocket] -= 1

            except websockets.exceptions.ConnectionClosed:
                disconnected.append(websocket)
            except Exception as e:
                logger.error(f"Broadcast error: {e}")
                disconnected.append(websocket)

        # Clean up disconnected clients
        for websocket in disconnected:
            self._subscribers[channel].discard(websocket)
            if websocket in self._buffer_sizes:
                del self._buffer_sizes[websocket]

    async def handle_client(self, websocket, path):
        """Handle a new WebSocket client connection."""
        client_channels = set()
        try:
            async for message in websocket:
                data = json.loads(message)
                action = data.get("action")
                channel = data.get("channel")

                if action == "subscribe":
                    await self.subscribe(websocket, channel)
                    client_channels.add(channel)

                elif action == "unsubscribe":
                    await self.unsubscribe(websocket, channel)
                    client_channels.discard(channel)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Client error: {e}")
        finally:
            # Clean up on disconnect
            for channel in list(client_channels):
                await self.unsubscribe(websocket, channel)
            logger.info("Client disconnected")


async def data_producer(server: RealTimeServer):
    """Simulate real-time stock price updates."""
    while True:
        try:
            # Pick a random stock
            stock = random.choice(STOCKS)
            
            # Simulate price movement (+/- 0.1% to 1%)
            change = random.uniform(-0.01, 0.01)
            STOCK_PRICES[stock] *= (1 + change)
            
            # Create message
            message = {
                "stock": stock,
                "price": round(STOCK_PRICES[stock], 2),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            # Broadcast to subscribers
            await server.broadcast(stock, message)
            
            await asyncio.sleep(0.5)
        except Exception as e:
            logger.error(f"Producer error: {e}")


async def main():
    """Start the WebSocket server."""
    server = RealTimeServer()

    async with websockets.serve(server.handle_client, "localhost", 8765):
        logger.info("WebSocket server started on ws://localhost:8765")
        logger.info("Open client.html in your browser to subscribe to stock updates")
        
        # Run data producer in background
        producer_task = asyncio.create_task(data_producer(server))
        
        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            logger.info("Server shutting down...")
            producer_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
