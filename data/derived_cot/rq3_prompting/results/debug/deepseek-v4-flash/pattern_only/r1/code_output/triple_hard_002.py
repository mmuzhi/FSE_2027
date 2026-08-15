from typing import List
from math import isqrt

class Solution:
    def componentValue(self, nums: List[int], edges: List[List[int]]) -> int:
        n = len(nums)
        tree = [[] for _ in range(n)]
        for u, v in edges:
            tree[u].append(v)
            tree[v].append(u)

        total = sum(nums)

        def dfs(u: int, p: int, target: int) -> int:
            cur = nums[u]
            for v in tree[u]:
                if v != p:
                    cur += dfs(v, u, target)
            return 0 if cur == target else cur

        divisors = []
        for x in range(1, isqrt(total) + 1):
            if total % x == 0:
                divisors.append(x)
                if x != total // x:
                    divisors.append(total // x)
        divisors.sort()

        for target in divisors:
            if target == total:
                continue
            if dfs(0, -1, target) == 0:
                return total // target - 1

        return 0