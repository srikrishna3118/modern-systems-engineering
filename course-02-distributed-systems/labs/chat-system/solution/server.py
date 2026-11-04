"""
Chat System - gRPC Server (Solution)

Complete implementation of the gRPC chat server with:
- Message sending and storage
- Bidirectional streaming for real-time chat
- User connection management
- Message history retrieval
"""

import os
import time
import uuid
import logging
from concurrent import futures
from collections import defaultdict
from threading import Lock
from queue import Queue, Empty

import grpc
import chat_pb2
import chat_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageStore:
    """In-memory message storage."""

    def __init__(self):
        self._messages = defaultdict(list)
        self._lock = Lock()

    def add_message(self, message: chat_pb2.ChatMessage) -> str:
        with self._lock:
            msg_id = str(uuid.uuid4())
            message.id = msg_id
            message.timestamp = int(time.time() * 1000)
            self._messages[message.room_id].append(message)
            logger.info(f"Stored message {msg_id} in room {message.room_id}")
            return msg_id

    def get_history(self, room_id: str, limit: int = 50, before_timestamp: int = 0) -> list:
        with self._lock:
            messages = self._messages.get(room_id, [])
            if before_timestamp > 0:
                messages = [m for m in messages if m.timestamp < before_timestamp]
            return messages[-limit:]


class RoomManager:
    """Manages chat rooms, connected users, and broadcast streams."""

    def __init__(self):
        self._rooms = defaultdict(dict)  # room_id -> {session_id: User}
        self._queues = defaultdict(list)  # room_id -> [Queue] for broadcasting
        self._lock = Lock()

    def add_user(self, room_id: str, user_id: str, user_name: str) -> str:
        with self._lock:
            session_id = str(uuid.uuid4())
            user = chat_pb2.User(
                user_id=user_id,
                user_name=user_name,
                online=True
            )
            self._rooms[room_id][session_id] = user
            logger.info(f"User {user_name} joined room {room_id} (session: {session_id})")
            return session_id

    def remove_user(self, session_id: str) -> bool:
        with self._lock:
            for room_id, sessions in self._rooms.items():
                if session_id in sessions:
                    user = sessions.pop(session_id)
                    logger.info(f"User {user.user_name} left room {room_id}")
                    return True
            return False

    def get_users(self, room_id: str) -> list:
        with self._lock:
            return list(self._rooms.get(room_id, {}).values())

    def register_queue(self, room_id: str) -> Queue:
        """Register a message queue for a client stream."""
        q = Queue()
        with self._lock:
            self._queues[room_id].append(q)
        return q

    def unregister_queue(self, room_id: str, q: Queue):
        with self._lock:
            if q in self._queues[room_id]:
                self._queues[room_id].remove(q)

    def broadcast(self, room_id: str, message: chat_pb2.ChatMessage, exclude_queue: Queue = None):
        """Broadcast a message to all streams in a room."""
        with self._lock:
            queues = list(self._queues.get(room_id, []))
        for q in queues:
            if q is not exclude_queue:
                q.put(message)


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    """Implements the ChatService gRPC service."""

    def __init__(self, message_store: MessageStore, room_manager: RoomManager):
        self._store = message_store
        self._rooms = room_manager

    def SendMessage(self, request, context):
        """Handle a single message send."""
        msg_id = self._store.add_message(request)
        # Broadcast to all connected streams
        self._rooms.broadcast(request.room_id, request)
        return chat_pb2.SendResponse(success=True, message_id=msg_id)

    def ChatStream(self, request_iterator, context):
        """
        Bidirectional streaming RPC for real-time chat.

        Receives messages from a client and broadcasts them to all
        other clients in the same room.
        """
        room_id = None
        message_queue = None

        try:
            for message in request_iterator:
                # Determine room from first message
                if room_id is None:
                    room_id = message.room_id
                    message_queue = self._rooms.register_queue(room_id)
                    logger.info(f"Stream opened for room {room_id}")

                # Store and broadcast
                self._store.add_message(message)
                self._rooms.broadcast(room_id, message, exclude_queue=message_queue)

                # Also yield any messages from other clients
                while True:
                    try:
                        queued_msg = message_queue.get_nowait()
                        yield queued_msg
                    except Empty:
                        break

                # Echo confirmation
                yield message

        except Exception as e:
            logger.error(f"Stream error: {e}")
        finally:
            if room_id and message_queue:
                self._rooms.unregister_queue(room_id, message_queue)
                logger.info(f"Stream closed for room {room_id}")

    def GetHistory(self, request, context):
        """Retrieve message history for a room."""
        messages = self._store.get_history(
            request.room_id,
            request.limit if request.limit > 0 else 50,
            request.before_timestamp
        )
        return chat_pb2.HistoryResponse(messages=messages)


class UserServiceServicer(chat_pb2_grpc.UserServiceServicer):
    """Implements the UserService gRPC service."""

    def __init__(self, room_manager: RoomManager):
        self._rooms = room_manager

    def Connect(self, request, context):
        session_id = self._rooms.add_user(
            request.room_id, request.user_id, request.user_name
        )
        return chat_pb2.ConnectResponse(success=True, session_id=session_id)

    def Disconnect(self, request, context):
        success = self._rooms.remove_user(request.session_id)
        return chat_pb2.DisconnectResponse(success=success)

    def ListUsers(self, request, context):
        users = self._rooms.get_users(request.room_id)
        return chat_pb2.ListUsersResponse(users=users)


def serve(port: int = 50051):
    """Start the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    message_store = MessageStore()
    room_manager = RoomManager()

    chat_pb2_grpc.add_ChatServiceServicer_to_server(
        ChatServiceServicer(message_store, room_manager), server
    )
    chat_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(room_manager), server
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"Chat server started on port {port}")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        logger.info("Server stopped")


if __name__ == "__main__":
    serve(port=int(os.environ.get("PORT", "50051")))
