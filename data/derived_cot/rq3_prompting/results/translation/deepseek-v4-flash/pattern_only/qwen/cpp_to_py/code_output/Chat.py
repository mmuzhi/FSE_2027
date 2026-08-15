import datetime

class Chat:
    class Message:
        def __init__(self, sender, receiver, message, timestamp):
            self.sender = sender
            self.receiver = receiver
            self.message = message
            self.timestamp = timestamp

    def __init__(self):
        self._users = {}

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
        self._users[sender].append(Chat.Message(sender, receiver, message, timestamp))
        self._users[receiver].append(Chat.Message(sender, receiver, message, timestamp))
        return True

    def get_messages(self, username):
        if username not in self._users:
            return []
        return [Chat.Message(m.sender, m.receiver, m.message, m.timestamp)
                for m in self._users[username]]

    def get_users(self):
        return {
            user: [Chat.Message(m.sender, m.receiver, m.message, m.timestamp)
                   for m in msgs]
            for user, msgs in self._users.items()
        }

    def get_current_time(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")