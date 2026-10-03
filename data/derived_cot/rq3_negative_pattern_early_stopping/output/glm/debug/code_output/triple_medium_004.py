class Solution:
    def kthLargestLevelSum(self, root: Optional[TreeNode], k: int) -> int:
        if not root:
            return -1
        dq = collections.deque([root])
        a = []
        while dq:
            lvlsum = 0
            for i in range(len(dq)):
               n = dq.popleft()
               lvlsum += n.val
               if n.left: dq.append(n.left)
               if n.right: dq.append(n.right)
                
            a.append(lvlsum) 
        a.sort(reverse=True)
        return a[k-1] if len(a) >= k else -1