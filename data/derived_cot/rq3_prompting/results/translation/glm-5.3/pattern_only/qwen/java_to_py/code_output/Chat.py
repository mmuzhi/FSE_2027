from datetime import datetime


class Chat:
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

        def __eq__(self, other):
            if self is other:
                return True
            if not isinstance(other, Chat.Message):
                return False
            return (self.sender == other.sender
                    and self.receiver == other.receiver
                    and self.message == other.message
                    and self.timestamp == other.timestamp)

        def __hash__(self):
            return hash((self.sender, self.receiver, self.message, self.timestamp))

        def __repr__(self):
            return ("Message{sender='%s', receiver='%s', message='%s', timestamp='%s'}"
                    % (self.sender, self.receiver, self.message, self.timestamp))

    def __init__(self):
        self.users = {}

    def add_user(self, username):
        if username in self.users:
            return False
        self.users[username] = []
        return True

    def remove_user(self, username):
        if username in self.users:
            del self.users[username]
            return True
        return False

    def send_message(self, sender, receiver, message):
        if sender not in self.users or receiver not in self.users:
            return False

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message_info = Chat.Message(sender, receiver, message, timestamp)

        self.users[sender].append(message_info)
        self.users[receiver].append(message_info)
        return True

    def get_messages(self, username):
        if username not in self.users:
            return []
        return self.users[username]

    def get_users(self):
        return self.users