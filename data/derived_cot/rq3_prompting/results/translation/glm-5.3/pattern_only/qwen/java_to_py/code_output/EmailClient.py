from datetime import datetime


class EmailClient:
    def __init__(self, addr, capacity):
        self.addr = addr
        self.capacity = capacity
        self.inbox = []

    def send_to(self, recv, content, size):
        if not recv.is_full_with_one_more_email(size):
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
            self.clear_inbox(size)
            if recv.is_full_with_one_more_email(size):
                return False
            return self.send_to(recv, content, size)  # Retry sending after clearing

    def fetch(self):
        if not self.inbox:
            return None
        for email in self.inbox:
            if email.get("state") == "unread":
                email["state"] = "read"
                return email
        return None

    def is_full_with_one_more_email(self, size):
        occupied_size = self.get_occupied_size()
        return occupied_size + size > self.capacity

    def get_occupied_size(self):
        occupied_size = 0
        for email in self.inbox:
            size_obj = email.get("size")
            if isinstance(size_obj, (int, float)):
                occupied_size += float(size_obj)
        return occupied_size

    def clear_inbox(self, size):
        if not self.addr:
            return
        freed_space = 0
        while freed_space < size and self.inbox:
            email = self.inbox.pop(0)
            size_obj = email.get("size")
            if isinstance(size_obj, (int, float)):
                freed_space += float(size_obj)

    def get_inbox(self):
        return self.inbox

    def set_inbox(self, inbox):
        self.inbox = inbox