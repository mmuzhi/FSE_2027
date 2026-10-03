from typing import List, Optional


class Solution:
    def splitListToParts(self, head: Optional[ListNode], k: int) -> List[Optional[ListNode]]:
        length = 0
        ptr = head
        while ptr:
            length += 1
            ptr = ptr.next

        arrange = []
        maxi = length // k
        remain = length % k

        for i in range(k):
            if remain:
                arrange.append(maxi + 1)  # add 1 till the remainder becomes 0
                remain -= 1
            else:
                arrange.append(maxi)

        result = []
        j = 0
        ptr = head
        i = 0
        while ptr:
            q = ptr
            i += 1
            ptr = ptr.next
            if i == arrange[j]:
                q.next = None
                result.append(head)
                head = ptr
                i = 0
                j += 1

        for _ in range(j, k):
            result.append(None)
        return result