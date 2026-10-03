import time
from collections import defaultdict

class Chat:
    class Message:
        def __init__(self, sender, receiver, message, timestamp):
            self.sender = sender
            self.receiver = receiver
            self.message = message
            self.timestamp = timestamp

    def __init__(self):
        self._users = defaultdict(list)  # {username: [Message, ...]}

    def add_user(self, username):
        if username in self._users:
            return False
        self._users[username] = []
        return True

    def remove_user(self, username):
        if username in self._users:
            del self._users[username]
            return True
        return False

    def send_message(self, sender, receiver, message):
        if sender not in self._users or receiver not in self._users:
            return False
        timestamp = self.get_current_time()
        msg = Chat.Message(sender, receiver, message, timestamp)
        self._users[sender].append(msg)
        self._users[receiver].append(msg)
        return True

    def get_messages(self, username):
        if username not in self._users:
            return []
        return list(self._users[username])

    def get_users(self):
        return dict(self._users)

    def get_current_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())