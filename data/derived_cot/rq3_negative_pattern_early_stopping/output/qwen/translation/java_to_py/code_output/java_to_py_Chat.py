import datetime
from typing import Dict, List, Optional

class Chat:
    class Message:
        def __init__(self, sender: str, receiver: str, message: str, timestamp: str):
            self.sender = sender
            self.receiver = receiver
            self.message = message
            self.timestamp = timestamp

        def getSender(self) -> str:
            return self.sender

        def getReceiver(self) -> str:
            return self.receiver

        def getMessage(self) -> str:
            return self.message

        def getTimestamp(self) -> str:
            return self.timestamp

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, Chat.Message):
                return False
            return (self.sender == other.sender and
                    self.receiver == other.receiver and
                    self.message == other.message and
                    self.timestamp == other.timestamp)

        def __hash__(self) -> int:
            return hash((self.sender, self.receiver, self.message, self.timestamp))

        def __repr__(self) -> str:
            return (f"Message(sender='{self.sender}', receiver='{self.receiver}', "
                    f"message='{self.message}', timestamp='{self.timestamp}')")

    def __init__(self):
        self.users: Dict[str, List[Chat.Message]] = {}

    def addUser(self, username: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = []
        return True

    def removeUser(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            return True
        return False

    def sendMessage(self, sender: str, receiver: str, message: str) -> bool:
        if sender not in self.users or receiver not in self.users:
            return False

        # Format the current time
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        msg = Chat.Message(sender, receiver, message, timestamp)
        self.users[sender].append(msg)
        self.users[receiver].append(msg)
        return True

    def getMessages(self, username: str) -> List[Chat.Message]:
        if username not in self.users:
            return []
        return self.users[username]

    def getUsers(self) -> Dict[str, List[Chat.Message]]:
        return self.users