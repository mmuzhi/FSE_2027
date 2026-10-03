from typing import List

class Solution:
    def edgeScore(self, edges: List[int]) -> int:
        n = len(edges)
        sc = [0] * n
        mx = -1
        ans = n
        for i in range(n):
            node = edges[i]
            sc[node] += i
            if sc[node] > mx:
                mx = sc[node]
                ans = node
            elif sc[node] == mx:
                if node < ans:
                    ans = node
        return ans