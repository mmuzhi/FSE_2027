from datetime import datetime


class Message:
    def __init__(self, sender, receiver, message, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.timestamp = timestamp

    def get_sender(self):
        return self.sender

    def get_receiver(self):
        return self.receiver

    def get_message(self):
        return self.message

    def get_timestamp(self):
        return self.timestamp

    def __eq__(self, obj):
        if self is obj:
            return True
        if obj is None or not isinstance(obj, Message):
            return False
        return (self.sender == obj.sender and
                self.receiver == obj.receiver and
                self.message == obj.message and
                self.timestamp == obj.timestamp)

    def __hash__(self):
        return hash((self.sender, self.receiver, self.message, self.timestamp))

    def __str__(self):
        return f"Message{{sender='{self.sender}', receiver='{self.receiver}', message='{self.message}', timestamp='{self.timestamp}'}}"


class Chat:
    def __init__(self):
        self.users = {}

    def add_user(self, username):
        if username in self.users:
            return False
        else:
            self.users[username] = []
            return True

    def remove_user(self, username):
        if username in self.users:
            del self.users[username]
            return True
        else:
            return False

    def send_message(self, sender, receiver, message):
        if sender not in self.users or receiver not in self.users:
            return False

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message_info = Message(sender, receiver, message, timestamp)

        self.users[sender].append(message_info)
        self.users[receiver].append(message_info)
        return True

    def get_messages(self, username):
        if username not in self.users:
            return []
        return self.users[username]

    def get_users(self):
        return self.users