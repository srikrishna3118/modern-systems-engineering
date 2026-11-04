"""
End-to-end check for the reference server.

Starts the server, subscribes two clients to AAPL, and confirms both
receive a tick. A third client with a queue of size 1 must not stop
the others when it stops reading.

    python smoke_client.py
"""

import asyncio
import json

import websockets

from server import STOCKS, RealTimeServer, data_producer


async def _collect(websocket, count: int, timeout: float = 3.0):
    messages = []
    while len(messages) < count:
        raw = await asyncio.wait_for(websocket.recv(), timeout=timeout)
        messages.append(json.loads(raw))
    return messages


async def main():
    app = RealTimeServer(max_backlog=8)
    slow = RealTimeServer(max_backlog=1)

    async with websockets.serve(app.handle_client, "127.0.0.1", 8765):
        producer = asyncio.create_task(data_producer(app, interval=0.05))
        try:
            async with websockets.connect("ws://127.0.0.1:8765") as left, websockets.connect(
                "ws://127.0.0.1:8765"
            ) as right:
                for socket in (left, right):
                    await socket.send(json.dumps({"action": "subscribe", "channel": "AAPL"}))
                left_msgs, right_msgs = await asyncio.gather(
                    _collect(left, 2),
                    _collect(right, 2),
                )
        finally:
            producer.cancel()

    for batch in (left_msgs, right_msgs):
        if any(message.get("stock") != "AAPL" for message in batch):
            raise SystemExit(f"unexpected payload: {batch}")
        if not all("price" in message for message in batch):
            raise SystemExit(f"missing price: {batch}")

    # A full queue drops for that client only. publish() must return.
    class _Socket:
        pass

    stuck = _Socket()
    other = _Socket()
    slow.subscribe(stuck, "AAPL")
    slow.subscribe(other, "AAPL")
    # Fill the stuck client, then keep publishing. The other client still gets copies
    # until its own queue fills; we only assert the call does not block.
    for _ in range(10):
        slow.publish("AAPL", {"stock": "AAPL", "price": 1.0, "timestamp": "t"})
    if slow.dropped == 0:
        raise SystemExit("expected the slow subscriber to drop updates")

    print(f"websocket smoke ok ({len(STOCKS)} symbols, dropped={slow.dropped})")


if __name__ == "__main__":
    asyncio.run(main())
