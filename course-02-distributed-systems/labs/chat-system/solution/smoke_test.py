"""Start the reference server and exercise both gRPC services.

    python -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/chat.proto
    python smoke_test.py
"""

import os
import socket
import subprocess
import sys
import time

import grpc

import chat_pb2
import chat_pb2_grpc


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def main():
    port = _free_port()
    env = os.environ.copy()
    env["PORT"] = str(port)
    proc = subprocess.Popen(
        [sys.executable, "server.py"],
        env=env,
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )
    channel = grpc.insecure_channel(f"127.0.0.1:{port}")
    try:
        grpc.channel_ready_future(channel).result(timeout=10)
        chat = chat_pb2_grpc.ChatServiceStub(channel)
        users = chat_pb2_grpc.UserServiceStub(channel)

        connected = users.Connect(
            chat_pb2.ConnectRequest(user_id="ada", user_name="Ada", room_id="general")
        )
        if not connected.success or not connected.session_id:
            raise SystemExit("connect failed")

        listing = users.ListUsers(chat_pb2.ListUsersRequest(room_id="general"))
        names = [user.user_name for user in listing.users]
        if "Ada" not in names:
            raise SystemExit(f"missing user: {names}")

        sent = chat.SendMessage(
            chat_pb2.ChatMessage(room_id="general", sender_name="Ada", content="hello")
        )
        if not sent.success or not sent.message_id:
            raise SystemExit("send failed")

        history = chat.GetHistory(chat_pb2.HistoryRequest(room_id="general", limit=10))
        contents = [message.content for message in history.messages]
        if "hello" not in contents:
            raise SystemExit(f"history missing message: {contents}")

        # Same logical send retried: the server stores another message today.
        # The smoke test only checks that a second call still succeeds.
        again = chat.SendMessage(
            chat_pb2.ChatMessage(room_id="general", sender_name="Ada", content="hello")
        )
        if not again.success:
            raise SystemExit("retry send failed")

        gone = users.Disconnect(chat_pb2.DisconnectRequest(session_id=connected.session_id))
        if not gone.success:
            raise SystemExit("disconnect failed")
        print("chat smoke ok")
    finally:
        channel.close()
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
