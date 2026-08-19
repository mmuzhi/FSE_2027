import time
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Message:
    sender: str
    receiver: str
    message: str
    timestamp: str


class Chat:
    def __init__(self) -> None:
        self.users: Dict[str, List[Message]] = {}

    def add_user(self, username: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = []
        return True

    def remove_user(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            return True
        return False

    def send_message(self, sender: str, receiver: str, message: str) -> bool:
        if sender not in self.users or receiver not in self.users:
            return False

        timestamp = self.get_current_time()
        message_info = Message(sender, receiver, message, timestamp)
        self.users[sender].append(message_info)
        self.users[receiver].append(message_info)
        return True

    def get_messages(self, username: str) -> List[Message]:
        if username not in self.users:
            return []
        return list(self.users[username])

    def get_users(self) -> Dict[str, List[Message]]:
        return {username: list(messages) for username, messages in self.users.items()}

    def get_current_time(self) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())