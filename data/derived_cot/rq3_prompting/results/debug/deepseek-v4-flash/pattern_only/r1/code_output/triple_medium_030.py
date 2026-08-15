from typing import Optional, List

class Solution:
    def splitListToParts(self, head: Optional[ListNode], k: int) -> List[Optional[ListNode]]:
        if k <= 0:
            return []

        length = 0
        curr = head
        while curr:
            length += 1
            curr = curr.next

        base = length // k
        extra = length % k

        result = []
        curr = head

        for i in range(k):
            part_size = base + (1 if i < extra else 0)

            if part_size == 0:
                result.append(None)
                continue

            result.append(curr)

            for _ in range(part_size - 1):
                curr = curr.next

            next_part = curr.next
            curr.next = None
            curr = next_part

        return result