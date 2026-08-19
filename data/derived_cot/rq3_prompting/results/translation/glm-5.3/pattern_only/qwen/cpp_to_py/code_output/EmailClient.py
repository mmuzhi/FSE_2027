import re
import time


def _stoi(s):
    # Mimics std::stoi: skips leading whitespace, parses optional sign + digits,
    # ignores trailing junk; raises ValueError when no digits are found.
    m = re.match(r"\s*([+-]?\d+)", s)
    if m is None:
        raise ValueError("stoi: no conversion")
    return int(m.group(1))


class EmailClient:
    def __init__(self, addr, capacity):
        self.addr = addr
        self.capacity = capacity
        self.inbox = []  # list of dicts, keys inserted alphabetically like std::map

    def get_current_time(self):
        ltm = time.localtime()
        return (f"{ltm.tm_year}-"
                f"{ltm.tm_mon}-"
                f"{ltm.tm_mday} "
                f"{ltm.tm_hour}:"
                f"{ltm.tm_min}:"
                f"{ltm.tm_sec}")

    def send_to(self, recv, content, size):
        if not recv.is_full_with_one_more_email(size):
            email = {
                "content": content,
                "receiver": recv.addr,
                "sender": self.addr,
                "size": str(size),
                "state": "unread",
                "time": self.get_current_time()
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
        return self.get_occupied_size() + size > self.capacity

    def get_occupied_size(self):
        occupied_size = 0
        for email in self.inbox:
            occupied_size += _stoi(email["size"])
        return occupied_size

    def clear_inbox(self, size):
        if not self.addr:
            return

        freed_space = 0
        while freed_space < size and self.inbox:
            freed_space += _stoi(self.inbox[0]["size"])
            del self.inbox[0]