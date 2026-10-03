class Solution:
    def splitListToParts(self, head: Optional[ListNode], k: int) -> List[Optional[ListNode]]:

    
        l = []
        length = 0
        ptr = head
        while(ptr) :
            length += 1
            ptr = ptr.next

        arrange = []
        maxi = length // k 
        remain = length % k

        for i in range(k) :
            if remain :
                arrange.append(maxi + 1)  
                remain -= 1
            else:
                arrange.append(maxi)

        j = 0
        ptr = head 
        i = 0
        while(ptr) :
            q = ptr 
            i += 1
            ptr = ptr.next 
            if i == arrange[j] :
                q.next = None
                l.append(head)
                head = ptr 
                i = 0
                j += 1

        for i in range(j, k):
            l.append(None)
        return l