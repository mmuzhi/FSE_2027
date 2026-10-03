from typing import Optional, List


class Solution:
    def splitListToParts(self, head: Optional[ListNode], k: int) -> List[Optional[ListNode]]:
        length = 0
        ptr = head
        while ptr:
            length += 1
            ptr = ptr.next

        base = length // k
        extra = length % k
        part_sizes = []
        for i in range(k):
            part_sizes.append(base + (1 if i < extra else 0))

        result = []
        ptr = head
        idx = 0
        while ptr:
            result.append(ptr)          # start of current part
            size = part_sizes[idx]
            for _ in range(size - 1):
                ptr = ptr.next
            next_part = ptr.next
            ptr.next = None
            ptr = next_part
            idx += 1

        while len(result) < k:
            result.append(None)

        return result