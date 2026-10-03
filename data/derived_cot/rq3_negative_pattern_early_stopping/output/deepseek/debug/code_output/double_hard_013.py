from typing import Optional

class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        currGroup = dummy

        while True:
            kth = self.getKth(currGroup, k)
            if not kth:
                break
            nextGroup = kth.next

            prev, curr = nextGroup, currGroup.next
            while curr != nextGroup:
                tmp = curr.next
                curr.next = prev
                prev = curr
                curr = tmp

            currGroup.next, currGroup = kth, currGroup.next

        return dummy.next

    def getKth(self, node: Optional[ListNode], k: int) -> Optional[ListNode]:
        while node and k:
            node = node.next
            k -= 1
        return node