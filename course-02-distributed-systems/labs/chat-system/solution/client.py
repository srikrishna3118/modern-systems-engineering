"""
Chat System - gRPC Client (Solution)

Complete client implementation with bidirectional streaming.
"""

import argparse
import threading
import logging

import grpc
import chat_pb2
import chat_pb2_grpc

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def send_messages(user_name: str, room_id: str):
    """Generator that reads user input and yields ChatMessage objects."""
    while True:
        try:
            text = input()
            if text.strip() == "/quit":
                print("Disconnecting...")
                return
            yield chat_pb2.ChatMessage(
                room_id=room_id,
                sender_name=user_name,
                content=text,
            )
        except EOFError:
            return


def receive_messages(response_iterator):
    """Reads messages from the server stream and prints them."""
    try:
        for message in response_iterator:
            print(f"[{message.sender_name}] {message.content}")
    except grpc.RpcError as e:
        if e.code() != grpc.StatusCode.CANCELLED:
            logger.error(f"Stream error: {e}")


def print_history(stub, room_id: str, limit: int = 20):
    """Fetch and display recent message history."""
    try:
        response = stub.GetHistory(
            chat_pb2.HistoryRequest(room_id=room_id, limit=limit)
        )
        if response.messages:
            print(f"\n--- Last {len(response.messages)} messages in #{room_id} ---")
            for msg in response.messages:
                print(f"  [{msg.sender_name}] {msg.content}")
            print("--- End of history ---\n")
        else:
            print(f"\nNo message history in #{room_id}\n")
    except grpc.RpcError as e:
        logger.error(f"Failed to fetch history: {e}")


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
    connect_response = user_stub.Connect(
        chat_pb2.ConnectRequest(
            user_id=args.user,
            user_name=args.user,
            room_id=args.room,
        )
    )
    print(f"Connected to #{args.room} as '{args.user}' (session: {connect_response.session_id})")

    # Show recent history
    print_history(chat_stub, args.room)

    # Start bidirectional streaming
    message_gen = send_messages(args.user, args.room)
    response_iterator = chat_stub.ChatStream(message_gen)

    # Receive messages in background thread
    recv_thread = threading.Thread(target=receive_messages, args=(response_iterator,), daemon=True)
    recv_thread.start()

    print("Type messages or /quit to exit.")

    # Wait for the generator to finish (user types /quit or EOF)
    recv_thread.join()

    # Disconnect
    user_stub.Disconnect(
        chat_pb2.DisconnectRequest(session_id=connect_response.session_id)
    )
    print("Disconnected.")


if __name__ == "__main__":
    main()
