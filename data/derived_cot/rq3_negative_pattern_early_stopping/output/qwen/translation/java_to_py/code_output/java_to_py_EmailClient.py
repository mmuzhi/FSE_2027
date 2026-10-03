import datetime
from typing import List, Dict, Any, Optional

class EmailClient:
    def __init__(self, addr: str, capacity: float):
        self.addr = addr
        self.capacity = capacity
        self.inbox: List[Dict[str, Any]] = []

    def send_to(self, recv: 'EmailClient', content: str, size: float) -> bool:
        if not recv.is_full_with_one_more_email(size):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            email = {
                'sender': self.addr,
                'receiver': recv.addr,
                'content': content,
                'size': size,
                'time': timestamp,
                'state': 'unread'
            }
            recv.inbox.append(email)
            return True
        else:
            self.clear_inbox(size)
            if recv.is_full_with_one_more_email(size):
                return False
            return self.send_to(recv, content, size)

    def fetch(self) -> Optional[Dict[str, Any]]:
        if not self.inbox:
            return None
        for email in self.inbox:
            if email['state'] == 'unread':
                email['state'] = 'read'
                return email
        return None

    def is_full_with_one_more_email(self, size: float) -> bool:
        occupied_size = self.get_occupied_size()
        return occupied_size + size > self.capacity

    def get_occupied_size(self) -> float:
        occupied_size = 0.0
        for email in self.inbox:
            if isinstance(email['size'], (int, float)):
                occupied_size += email['size']
        return occupied_size

    def clear_inbox(self, size: float) -> None:
        if not self.addr:
            return
        freed_space = 0.0
        while freed_space < size and self.inbox:
            email = self.inbox.pop(0)
            freed_space += email['size']

    def get_inbox(self) -> List[Dict[str, Any]]:
        return self.inbox

    def set_inbox(self, inbox: List[Dict[str, Any]]) -> None:
        self.inbox = inbox