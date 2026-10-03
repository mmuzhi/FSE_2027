import datetime

class EmailClient:
    def __init__(self, addr: str, capacity: float):
        self.addr = addr
        self.capacity = capacity
        self.inbox = []

    def send_to(self, recv: 'EmailClient', content: str, size: float) -> bool:
        if not recv.is_full_with_one_more_email(size):
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
            self.clear_inbox(size)
            if recv.is_full_with_one_more_email(size):
                return False
            return self.send_to(recv, content, size)

    def fetch(self):
        if not self.inbox:
            return None
        for email in self.inbox:
            if email.get("state") == "unread":
                email["state"] = "read"
                return email
        return None

    def is_full_with_one_more_email(self, size: float) -> bool:
        occupied = self.get_occupied_size()
        return occupied + size > self.capacity

    def get_occupied_size(self) -> float:
        total = 0.0
        for email in self.inbox:
            sz = email.get("size")
            if isinstance(sz, (int, float)):
                total += float(sz)
        return total

    def clear_inbox(self, size: float):
        if not self.addr:
            return
        freed = 0.0
        while freed < size and self.inbox:
            email = self.inbox.pop(0)
            sz = email.get("size")
            if isinstance(sz, (int, float)):
                freed += float(sz)

    def get_inbox(self):
        return self.inbox

    def set_inbox(self, inbox):
        self.inbox = inbox