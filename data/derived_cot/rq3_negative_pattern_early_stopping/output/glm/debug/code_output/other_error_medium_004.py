class Solution:
    def kthLargestLevelSum(self, root: Optional[TreeNode], k: int) -> int:
        dq = collections.deque([root])
        a = []
        lvl = 1
        while dq:
            lvlsum = 0
            for i in range(len(dq)):
               n = dq.popleft()
               lvlsum += n.val
               if n.left: dq.append(n.left)
               if n.right: dq.append(n.right)
            a.append(lvlsum)
            lvl += 1
        a.sort(reverse=True)
        return a[k-1] if len(a) >= k else -1