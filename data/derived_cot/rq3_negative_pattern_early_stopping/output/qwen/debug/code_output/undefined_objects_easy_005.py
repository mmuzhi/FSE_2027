# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def findMode(self, root: Optional[TreeNode]) -> List[int]:
        from collections import deque
        freq = {}
        if not root:
            return []
        
        queue = deque([root])
        while queue:
            curr = queue.popleft()
            freq[curr.val] = freq.get(curr.val, 0) + 1
            if curr.left:
                queue.append(curr.left)
            if curr.right:
                queue.append(curr.right)
        
        max_cnt = 0
        ans = []
        for val, cnt in freq.items():
            if cnt > max_cnt:
                max_cnt = cnt
                ans = [val]
            elif cnt == max_cnt:
                ans.append(val)
        return ans