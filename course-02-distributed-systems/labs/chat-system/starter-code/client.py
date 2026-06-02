"""
Chat System - gRPC Client (Starter Code)

A simple client to connect to the chat server, send messages,
and receive messages via bidirectional streaming.

Usage:
  python client.py --user alice --room general
"""

import argparse
import threading
import time
import logging

import grpc
import chat_pb2
import chat_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_messages(stub, user_name: str, room_id: str):
    """
    Generator that reads user input and yields ChatMessage objects.
    This feeds the bidirectional stream.
    """
    # TODO: Implement a generator that:
    # 1. Reads input from the user (use input() in a loop)
    # 2. Creates a ChatMessage with room_id, sender_name, and content
    # 3. Yields the message
    # 4. Stops when user types '/quit'
    pass


def receive_messages(response_iterator):
    """
    Reads messages from the server stream and prints them.
    Runs in a background thread.
    """
    # TODO: Iterate over response_iterator and print each message
    # Format: [sender_name] content
    pass


def print_history(stub, room_id: str, limit: int = 20):
    """Fetch and display recent message history."""
    # TODO: Call stub.GetHistory() and print the messages
    pass


def main():
    parser = argparse.ArgumentParser(description="Chat Client")
    parser.add_argument("--user", required=True, help="Your username")
    parser.add_argument("--room", default="general", help="Chat room to join")
    parser.add_argument("--host", default="localhost:50051", help="Server address")
    args = parser.parse_args()

    channel = grpc.insecure_channel(args.host)
    chat_stub = chat_pb2_grpc.ChatServiceStub(channel)
    user_stub = chat_pb2_grpc.UserServiceStub(channel)

    # Connect to room
    # TODO: Call user_stub.Connect() to register the user
    # Print confirmation with session_id

    # Show recent history
    print_history(chat_stub, args.room)

    # Start bidirectional streaming
    # TODO:
    # 1. Create the message generator: send_messages(chat_stub, args.user, args.room)
    # 2. Call chat_stub.ChatStream(generator) to get the response iterator
    # 3. Start receive_messages in a background thread
    # 4. Wait for the user to finish typing

    print(f"Connected to room '{args.room}' as '{args.user}'. Type messages or /quit to exit.")


if __name__ == "__main__":
    main()
