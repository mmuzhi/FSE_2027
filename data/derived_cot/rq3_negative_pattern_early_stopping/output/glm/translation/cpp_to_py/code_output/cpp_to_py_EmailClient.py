import datetime


class EmailClient:
    def __init__(self, addr, capacity):
        self.addr = addr
        self.capacity = capacity
        self.inbox = []

    def get_current_time(self):
        now = datetime.datetime.now()
        return f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}"

    def send_to(self, recv, content, size):
        if not recv.is_full_with_one_more_email(size):
            email = {
                "sender": self.addr,
                "receiver": recv.addr,
                "content": content,
                "size": str(size),
                "time": self.get_current_time(),
                "state": "unread",
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
                return email
        return {}

    def is_full_with_one_more_email(self, size):
        occupied_size = self.get_occupied_size()
        return occupied_size + size > self.capacity

    def get_occupied_size(self):
        occupied_size = 0
        for email in self.inbox:
            occupied_size += int(email["size"])
        return occupied_size

    def clear_inbox(self, size):
        if not self.addr:
            return

        freed_space = 0
        while freed_space < size and self.inbox:
            freed_space += int(self.inbox[0]["size"])
            del self.inbox[0]