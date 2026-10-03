class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        a = b = head
        while(a != None and a.next != None):
            b = b.next
            a = a.next.next
            if(a == b):
                return True
        return False