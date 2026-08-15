from typing import Optional

class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        currGroup = dummy

        while True:
            kth = self.getKth(currGroup, k)
            if kth is None:
                break
            nextGroup = kth.next

            prev, curr = kth.next, currGroup.next
            while curr is not nextGroup:
                tmp = curr.next
                curr.next = prev
                prev = curr
                curr = tmp

            tmp = currGroup.next
            currGroup.next = kth
            currGroup = tmp

        return dummy.next

    def getKth(self, node, k):
        while node and k > 0:
            node = node.next
            k -= 1
        return node