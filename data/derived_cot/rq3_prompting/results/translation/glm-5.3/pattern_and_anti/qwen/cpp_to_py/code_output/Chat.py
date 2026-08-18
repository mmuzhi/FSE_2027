import time
from dataclasses import dataclass


@dataclass
class Message:
    sender: str
    receiver: str
    message: str
    timestamp: str


class Chat:
    def __init__(self) -> None:
        self._users: dict[str, list[Message]] = {}

    def add_user(self, username: str) -> bool:
        if username in self._users:
            return False
        self._users[username] = []
        return True

    def remove_user(self, username: str) -> bool:
        if username in self._users:
            del self._users[username]
            return True
        return False

    def send_message(self, sender: str, receiver: str, message: str) -> bool:
        if sender not in self._users or receiver not in self._users:
            return False

        timestamp = self.get_current_time()
        message_info = Message(sender, receiver, message, timestamp)
        self._users[sender].append(message_info)
        self._users[receiver].append(message_info)
        return True

    def get_messages(self, username: str) -> list[Message]:
        if username not in self._users:
            return []
        return list(self._users[username])

    def get_users(self) -> dict[str, list[Message]]:
        return {username: list(messages) for username, messages in self._users.items()}

    def get_current_time(self) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())