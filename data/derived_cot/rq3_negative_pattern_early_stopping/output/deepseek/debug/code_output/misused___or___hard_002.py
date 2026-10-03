from typing import List

class Solution:
    def longestCycle(self, edges: List[int]) -> int:
        n = len(edges)
        v = [0] * n  # 0 = unvisited, otherwise [start_node, step]
        ans = -1
        for i in range(n):
            if v[i] != 0:
                continue
            t = 1
            c = i
            while c >= 0:
                if v[c] != 0:
                    if v[c][0] == i:  # cycle detected
                        ans = max(ans, t - v[c][1])
                    break
                else:
                    v[c] = [i, t]
                    t += 1
                    c = edges[c]
        return ans