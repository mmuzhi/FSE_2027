import datetime
import numbers

class EmailClient:
    def __init__(self, addr: str, capacity: float):
        self.addr = addr
        self.capacity = capacity
        self.inbox = []

    def sendTo(self, recv: 'EmailClient', content: str, size: float) -> bool:
        if not recv.isFullWithOneMoreEmail(size):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
            return self.sendTo(recv, content, size) # Retry sending after clearing

    def fetch(self):
        if not self.inbox:
            return None
        for email in self.inbox:
            if email.get("state") == "unread":
                email["state"] = "read"
                return email
        return None

    def isFullWithOneMoreEmail(self, size: float) -> bool:
        occupied_size = self.getOccupiedSize()
        return occupied_size + size > self.capacity

    def getOccupiedSize(self) -> float:
        occupied_size = 0.0
        for email in self.inbox:
            size_obj = email.get("size")
            if isinstance(size_obj, numbers.Number):
                occupied_size += float(size_obj)
        return occupied_size

    def clearInbox(self, size: float) -> None:
        if not self.addr:
            return
        freed_space = 0.0
        while freed_space < size and self.inbox:
            email = self.inbox.pop(0)
            size_obj = email.get("size")
            if isinstance(size_obj, numbers.Number):
                freed_space += float(size_obj)

    def getInbox(self):
        return self.inbox

    def setInbox(self, inbox):
        self.inbox = inbox