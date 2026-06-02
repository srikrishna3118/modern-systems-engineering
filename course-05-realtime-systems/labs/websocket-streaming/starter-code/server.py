"""
WebSocket Real-Time Streaming Server (Starter Code)

A simple WebSocket server that broadcasts real-time stock price updates
to multiple subscribers. Covers pub/sub patterns and backpressure handling.

Run:
  pip install -r requirements.txt
  python server.py
"""

import asyncio
import json
import logging
from datetime import datetime
from collections import defaultdict

# pip install websockets
import websockets

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


class RealTimeServer:
    """WebSocket server for real-time data streaming with pub/sub pattern."""

    def __init__(self):
        self._subscribers = defaultdict(set)  # channel -> {websocket}
        self._buffer_sizes = {}  # websocket -> current buffer size

    async def subscribe(self, websocket, channel: str):
        """
        TODO: Add a client to the subscribers set for a channel.
        
        Steps:
        1. Add websocket to self._subscribers[channel]
        2. Initialize buffer size: self._buffer_sizes[websocket] = 0
        3. Log subscription
        """
        pass

    async def unsubscribe(self, websocket, channel: str):
        """
        TODO: Remove a client from a channel's subscribers.
        
        Steps:
        1. Remove websocket from self._subscribers[channel]
        2. Clean up empty channels
        3. Remove from buffer_sizes
        """
        pass

    async def broadcast(self, channel: str, message: dict, max_backlog: int = 100):
        """
        TODO: Broadcast a message to all subscribers on a channel.
        
        Implement backpressure handling:
        1. For each subscriber on the channel:
           a. Increment buffer size
           b. If buffer size > max_backlog, drop the client (slow subscriber)
           c. Otherwise, send the message
           d. Decrement buffer size after send
        
        Hint: Use websocket.send() to send JSON-serialized message
        """
        pass

    async def handle_client(self, websocket, path):
        """
        TODO: Handle a new WebSocket client connection.
        
        Protocol:
        1. Client can send:
           - { "action": "subscribe", "channel": "AAPL" }
           - { "action": "unsubscribe", "channel": "AAPL" }
        2. Server broadcasts updates to subscribers
        
        Steps:
        1. Read messages in a loop (async for message in websocket)
        2. Parse JSON
        3. If action == "subscribe": call subscribe()
        4. If action == "unsubscribe": call unsubscribe()
        5. Handle client disconnect (asyncio.CancelledError, websockets.exceptions)
        """
        client_channels = set()
        try:
            async for message in websocket:
                data = json.loads(message)
                action = data.get("action")
                channel = data.get("channel")

                if action == "subscribe":
                    await self.subscribe(websocket, channel)
                    client_channels.add(channel)
                    logger.info(f"Client subscribed to {channel}")

                elif action == "unsubscribe":
                    await self.unsubscribe(websocket, channel)
                    client_channels.discard(channel)
                    logger.info(f"Client unsubscribed from {channel}")

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Client error: {e}")
        finally:
            # Clean up on disconnect
            for channel in client_channels:
                await self.unsubscribe(websocket, channel)
            logger.info(f"Client disconnected")


async def data_producer(server: RealTimeServer):
    """
    TODO: Simulate real-time stock price updates.
    
    Steps:
    1. Loop forever:
       a. Generate a random price update for a stock (e.g., AAPL, GOOGL)
       b. Create a message: { "stock": "AAPL", "price": 150.25, "timestamp": ... }
       c. Broadcast to all subscribers on that channel
       d. Sleep 0.5 seconds
    """
    pass


async def main():
    """Start the WebSocket server."""
    server = RealTimeServer()

    # Start WebSocket server
    async with websockets.serve(server.handle_client, "localhost", 8765):
        logger.info("WebSocket server started on ws://localhost:8765")
        
        # Run data producer in background
        # TODO: Create a task for data_producer(server)
        # producer_task = asyncio.create_task(data_producer(server))
        
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
