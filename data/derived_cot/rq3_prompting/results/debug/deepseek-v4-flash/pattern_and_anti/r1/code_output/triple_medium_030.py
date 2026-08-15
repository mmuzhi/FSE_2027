from typing import Optional, List

class Solution:
    def splitListToParts(self, head: Optional[ListNode], k: int) -> List[Optional[ListNode]]:
        l = []
        length = 0
        ptr = head
        while ptr:
            length += 1
            ptr = ptr.next

        arrange = []
        base = length // k
        remain = length % k

        for _ in range(k):
            if remain:
                arrange.append(base + 1)
                remain -= 1
            else:
                arrange.append(base)

        j = 0
        ptr = head
        i = 0

        while ptr:
            q = ptr
            i += 1
            ptr = ptr.next

            if i == arrange[j]:
                q.next = None
                l.append(head)
                head = ptr
                i = 0
                j += 1

        for _ in range(j, k):
            l.append(None)

        return l