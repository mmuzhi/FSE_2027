from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        currGroup = dummy

        while True:
            kth = self.getKth(currGroup, k)
            if not kth:
                break
            nextGroup = kth.next

            prev = nextGroup
            curr = currGroup.next
            while curr != nextGroup:
                tmp = curr.next
                curr.next = prev
                prev = curr
                curr = tmp

            start = currGroup.next
            currGroup.next = kth
            start.next = nextGroup
            currGroup = start

        return dummy.next

    def getKth(self, node: ListNode, k: int) -> Optional[ListNode]:
        while node and k:
            node = node.next
            k -= 1
        return node