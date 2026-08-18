from dataclasses import dataclass
from datetime import datetime


class Chat:
    @dataclass(frozen=True)
    class Message:
        sender: str
        receiver: str
        message: str
        timestamp: str

        def get_sender(self) -> str:
            return self.sender

        def get_receiver(self) -> str:
            return self.receiver

        def get_message(self) -> str:
            return self.message

        def get_timestamp(self) -> str:
            return self.timestamp

        def __repr__(self) -> str:
            return (f"Message{{sender='{self.sender}', receiver='{self.receiver}', "
                    f"message='{self.message}', timestamp='{self.timestamp}'}}")

    def __init__(self):
        self.users: dict[str, list[Chat.Message]] = {}

    def add_user(self, username: str) -> bool:
        if username in self.users:
            return False
        else:
            self.users[username] = []
            return True

    def remove_user(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            return True
        else:
            return False

    def send_message(self, sender: str, receiver: str, message: str) -> bool:
        if sender not in self.users or receiver not in self.users:
            return False

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message_info = Chat.Message(sender, receiver, message, timestamp)

        self.users[sender].append(message_info)
        self.users[receiver].append(message_info)
        return True

    def get_messages(self, username: str) -> list:
        if username not in self.users:
            return []
        return self.users[username]

    def get_users(self) -> dict:
        return self.users