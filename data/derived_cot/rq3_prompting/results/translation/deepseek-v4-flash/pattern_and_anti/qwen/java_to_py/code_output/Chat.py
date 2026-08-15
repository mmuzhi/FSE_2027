from datetime import datetime


class Chat:
    class Message:
        def __init__(self, sender, receiver, message, timestamp):
            self.sender = sender
            self.receiver = receiver
            self.message = message
            self.timestamp = timestamp

        def getSender(self):
            return self.sender

        def getReceiver(self):
            return self.receiver

        def getMessage(self):
            return self.message

        def getTimestamp(self):
            return self.timestamp

        @staticmethod
        def _to_java_string(value):
            return "null" if value is None else str(value)

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or type(self) != type(other):
                return False
            return (self.sender == other.sender and
                    self.receiver == other.receiver and
                    self.message == other.message and
                    self.timestamp == other.timestamp)

        def __hash__(self):
            return hash((self.sender, self.receiver, self.message, self.timestamp))

        def __repr__(self):
            return "Message{sender='%s', receiver='%s', message='%s', timestamp='%s'}" % (
                self._to_java_string(self.sender),
                self._to_java_string(self.receiver),
                self._to_java_string(self.message),
                self._to_java_string(self.timestamp),
            )

        __str__ = __repr__

    def __init__(self):
        self.users = {}

    def addUser(self, username):
        if username in self.users:
            return False
        self.users[username] = []
        return True

    def removeUser(self, username):
        if username in self.users:
            del self.users[username]
            return True
        return False

    def sendMessage(self, sender, receiver, message):
        if sender not in self.users or receiver not in self.users:
            return False
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_info = self.Message(sender, receiver, message, timestamp)
        self.users[sender].append(message_info)
        self.users[receiver].append(message_info)
        return True

    def getMessages(self, username):
        if username not in self.users:
            return []
        return self.users[username]

    def getUsers(self):
        return self.users