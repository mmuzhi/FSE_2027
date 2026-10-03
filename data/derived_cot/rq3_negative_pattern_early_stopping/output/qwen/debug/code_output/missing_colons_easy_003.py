class Solution:
    def findMode(self, root: Optional[TreeNode]) -> List[int]:
        from collections import defaultdict
        def bfs(freq):
            queue = [root]
            while queue:
                curr = queue.pop()
                if curr.left:
                    queue.append(curr.left)
                if curr.right:
                    queue.append(curr.right)
                freq[curr.val] += 1

        freq = defaultdict(int)
        bfs(freq)
        # Now, find the maximum frequency
        max_cnt = 0
        for num, cnt in freq.items():
            if cnt > max_cnt:
                max_cnt = cnt
        ans = []
        for num, cnt in freq.items():
            if cnt == max_cnt:
                ans.append(num)
        return ans