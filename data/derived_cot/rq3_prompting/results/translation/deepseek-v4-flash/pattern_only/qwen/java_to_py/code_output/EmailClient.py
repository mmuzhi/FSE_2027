from datetime import datetime

class EmailClient:
    def __init__(self, addr, capacity):
        self.addr = addr
        self.capacity = capacity
        self.inbox = []

    def sendTo(self, recv, content, size):
        if not recv.isFullWithOneMoreEmail(size):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            email = {
                "sender": self.addr,
                "receiver": recv.addr,
                "content": content,
                "size": size,
                "time": timestamp,
                "state": "unread"
            }
            recv.inbox.append(email)
            return True
        else:
            self.clearInbox(size)
            if recv.isFullWithOneMoreEmail(size):
                return False
            return self.sendTo(recv, content, size)

    def fetch(self):
        if not self.inbox:
            return None
        for email in self.inbox:
            if email.get("state") == "unread":
                email["state"] = "read"
                return email
        return None

    def isFullWithOneMoreEmail(self, size):
        occupiedSize = self.getOccupiedSize()
        return occupiedSize + size > self.capacity

    def getOccupiedSize(self):
        occupiedSize = 0.0
        for email in self.inbox:
            sizeObj = email.get("size")
            if isinstance(sizeObj, (int, float)) and not isinstance(sizeObj, bool):
                occupiedSize += sizeObj
        return occupiedSize

    def clearInbox(self, size):
        if self.addr == "":
            return
        freedSpace = 0.0
        while freedSpace < size and self.inbox:
            email = self.inbox.pop(0)
            sizeObj = email.get("size")
            if isinstance(sizeObj, (int, float)) and not isinstance(sizeObj, bool):
                freedSpace += sizeObj

    def getInbox(self):
        return self.inbox

    def setInbox(self, inbox):
        self.inbox = inbox