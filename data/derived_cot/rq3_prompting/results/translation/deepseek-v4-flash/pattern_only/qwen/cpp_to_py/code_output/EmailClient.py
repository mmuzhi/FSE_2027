import time


class EmailClient:
    def __init__(self, addr, capacity):
        self.addr = addr
        self.capacity = capacity
        self.inbox = []

    def get_current_time(self):
        now = time.localtime()
        return f"{now.tm_year}-{now.tm_mon}-{now.tm_mday} {now.tm_hour}:{now.tm_min}:{now.tm_sec}"

    def send_to(self, recv, content, size):
        if not recv.is_full_with_one_more_email(size):
            email = {
                "content": content,
                "receiver": recv.addr,
                "sender": self.addr,
                "size": str(size),
                "state": "unread",
                "time": self.get_current_time(),
            }
            recv.inbox.append(email)
            return True
        else:
            self.clear_inbox(size)
            return False

    def fetch(self):
        if not self.inbox:
            return {}
        for email in self.inbox:
            if email["state"] == "unread":
                email["state"] = "read"
                return email.copy()
        return {}

    def is_full_with_one_more_email(self, size):
        return self.get_occupied_size() + size > self.capacity

    def get_occupied_size(self):
        return sum(int(email["size"]) for email in self.inbox)

    def clear_inbox(self, size):
        if self.addr == "":
            return
        freed_space = 0
        while freed_space < size and self.inbox:
            freed_space += int(self.inbox[0]["size"])
            del self.inbox[0]