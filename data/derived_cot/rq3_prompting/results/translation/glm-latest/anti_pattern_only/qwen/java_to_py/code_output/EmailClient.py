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
                "state": "unread",
            }
            recv.inbox.append(email)
            return True
        else:
            self.clearInbox(size)
            if recv.isFullWithOneMoreEmail(size):
                return False
            return self.sendTo(recv, content, size)  # Retry sending after clearing

    def fetch(self):
        if not self.inbox:
            return None
        for email in self.inbox:
            if email.get("state") == "unread":
                email["state"] = "read"
                return email
        return None

    def isFullWithOneMoreEmail(self, size):
        occupied_size = self.getOccupiedSize()
        return occupied_size + size > self.capacity

    def getOccupiedSize(self):
        occupied_size = 0.0
        for email in self.inbox:
            size_obj = email.get("size")
            # Java: sizeObj instanceof Number (bool is not a Number in Java)
            if isinstance(size_obj, (int, float)) and not isinstance(size_obj, bool):
                occupied_size += float(size_obj)
        return occupied_size

    def clearInbox(self, size):
        if not self.addr:
            return
        freed_space = 0.0
        while freed_space < size and self.inbox:
            email = self.inbox.pop(0)
            size_obj = email.get("size")
            if isinstance(size_obj, (int, float)) and not isinstance(size_obj, bool):
                freed_space += float(size_obj)

    def getInbox(self):
        return self.inbox

    def setInbox(self, inbox):
        self.inbox = inbox