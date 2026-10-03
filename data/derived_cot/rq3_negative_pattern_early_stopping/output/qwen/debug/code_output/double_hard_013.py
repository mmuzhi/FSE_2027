class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        currGroup = dummy

        while True:
            first_node = currGroup.next
            if not first_node:
                break

            kth = self.getKth(first_node, k-1)
            if kth is None:
                break
            nextGroup = kth.next

            prev = None
            curr = first_node
            for _ in range(k):
                nxt = curr.next
                curr.next = prev
                prev = curr
                curr = nxt

            currGroup.next = prev
            currGroup = first_node

        return dummy.next

    def getKth(self, node, k):
        while node and k:
            node = node.next
            k -= 1
        return node