"""
Chat System - gRPC Server (Starter Code)

This is the starter code for the Chat System lab.
Implement the TODO sections to complete the gRPC chat server.

Architecture:
  Client → gRPC Server → ChatService (message handling)
                       → UserService (user management)

Run:
  pip install grpcio grpcio-tools
  python -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/chat.proto
  python server.py
"""

import time
import uuid
import logging
from concurrent import futures
from collections import defaultdict
from threading import Lock

import grpc

# These will be generated from chat.proto
# Run: python -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/chat.proto
import chat_pb2
import chat_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageStore:
    """In-memory message storage. In production, use a database."""

    def __init__(self):
        self._messages = defaultdict(list)  # room_id -> [ChatMessage]
        self._lock = Lock()

    def add_message(self, message: chat_pb2.ChatMessage) -> str:
        """Store a message and return its ID."""
        with self._lock:
            msg_id = str(uuid.uuid4())
            message.id = msg_id
            message.timestamp = int(time.time() * 1000)
            self._messages[message.room_id].append(message)
            return msg_id

    def get_history(self, room_id: str, limit: int = 50, before_timestamp: int = 0) -> list:
        """Retrieve message history for a room."""
        with self._lock:
            messages = self._messages.get(room_id, [])
            if before_timestamp > 0:
                messages = [m for m in messages if m.timestamp < before_timestamp]
            return messages[-limit:]


class RoomManager:
    """Manages chat rooms and connected users."""

    def __init__(self):
        self._rooms = defaultdict(dict)  # room_id -> {session_id: User}
        self._streams = defaultdict(list)  # room_id -> [context] for broadcasting
        self._lock = Lock()

    def add_user(self, room_id: str, user_id: str, user_name: str) -> str:
        """Add a user to a room. Returns session_id."""
        # TODO: Generate a session_id, create a User, and add to the room
        # Hint: Use uuid.uuid4() for session_id
        # Store in self._rooms[room_id][session_id]
        pass

    def remove_user(self, session_id: str) -> bool:
        """Remove a user from their room."""
        # TODO: Find and remove the user by session_id
        # Search through self._rooms to find which room the session belongs to
        pass

    def get_users(self, room_id: str) -> list:
        """Get all users in a room."""
        with self._lock:
            return list(self._rooms.get(room_id, {}).values())

    def register_stream(self, room_id: str, context):
        """Register a stream context for message broadcasting."""
        with self._lock:
            self._streams[room_id].append(context)

    def unregister_stream(self, room_id: str, context):
        """Unregister a stream context."""
        with self._lock:
            if context in self._streams[room_id]:
                self._streams[room_id].remove(context)

    def get_streams(self, room_id: str) -> list:
        """Get all active stream contexts for a room."""
        with self._lock:
            return list(self._streams.get(room_id, []))


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    """Implements the ChatService gRPC service."""

    def __init__(self, message_store: MessageStore, room_manager: RoomManager):
        self._store = message_store
        self._rooms = room_manager

    def SendMessage(self, request, context):
        """Handle a single message send."""
        # TODO: Store the message and return a SendResponse
        # 1. Call self._store.add_message(request)
        # 2. Return a SendResponse with success=True and the message_id
        pass

    def ChatStream(self, request_iterator, context):
        """
        Bidirectional streaming RPC for real-time chat.

        This is the core of the chat system. Clients send messages through
        the stream, and receive messages from other users in the same room.

        Implementation steps:
        1. Read the first message to determine the room_id
        2. Register this stream for broadcasting
        3. For each incoming message:
           a. Store the message
           b. Broadcast to all other streams in the room
        4. Clean up on disconnect
        """
        # TODO: Implement bidirectional streaming chat
        #
        # Hint: This is the most complex part. You need to:
        # - Use a queue (from queue import Queue) to decouple receiving and sending
        # - Start a thread that reads from request_iterator and puts messages in the queue
        # - Yield messages from the queue for broadcasting
        #
        # Simplified approach (single-direction for starter):
        # for message in request_iterator:
        #     self._store.add_message(message)
        #     yield message  # Echo back (replace with proper broadcasting)
        pass

    def GetHistory(self, request, context):
        """Retrieve message history for a room."""
        # TODO: Fetch messages from the store and return a HistoryResponse
        # 1. Call self._store.get_history(request.room_id, request.limit, request.before_timestamp)
        # 2. Return a HistoryResponse with the messages
        pass


class UserServiceServicer(chat_pb2_grpc.UserServiceServicer):
    """Implements the UserService gRPC service."""

    def __init__(self, room_manager: RoomManager):
        self._rooms = room_manager

    def Connect(self, request, context):
        """Register a user connection to a room."""
        # TODO: Add user to room and return ConnectResponse with session_id
        pass

    def Disconnect(self, request, context):
        """Disconnect a user."""
        # TODO: Remove user and return DisconnectResponse
        pass

    def ListUsers(self, request, context):
        """List all users in a room."""
        # TODO: Get users from room_manager and return ListUsersResponse
        pass


def serve(port: int = 50051):
    """Start the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Shared state
    message_store = MessageStore()
    room_manager = RoomManager()

    # Register services
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
    serve()
