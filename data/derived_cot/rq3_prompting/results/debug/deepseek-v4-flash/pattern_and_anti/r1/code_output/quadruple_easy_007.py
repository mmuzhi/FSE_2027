from typing import Optional

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        a = b = head
        while a is not None and a.next is not None:
            b = b.next
            a = a.next.next
            if a == b:
                return True
        return False