import datetime

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

        def __eq__(self, other):
            if self is other:
                return True
            if not isinstance(other, Chat.Message):
                return False
            return (self.sender == other.sender and
                    self.receiver == other.receiver and
                    self.message == other.message and
                    self.timestamp == other.timestamp)

        def __hash__(self):
            return hash((self.sender, self.receiver, self.message, self.timestamp))

        def __str__(self):
            return f"Message{{sender='{self.sender}', receiver='{self.receiver}', message='{self.message}', timestamp='{self.timestamp}'}}"

        def __repr__(self):
            return self.__str__()

    def __init__(self):
        self.users = {}

    def addUser(self, username):
        if username in self.users:
            return False
        else:
            self.users[username] = []
            return True

    def removeUser(self, username):
        if username in self.users:
            del self.users[username]
            return True
        else:
            return False

    def sendMessage(self, sender, receiver, message):
        if sender not in self.users or receiver not in self.users:
            return False
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = Chat.Message(sender, receiver, message, timestamp)
        self.users[sender].append(msg)
        self.users[receiver].append(msg)
        return True

    def getMessages(self, username):
        if username not in self.users:
            return []
        return self.users[username]

    def getUsers(self):
        return self.users