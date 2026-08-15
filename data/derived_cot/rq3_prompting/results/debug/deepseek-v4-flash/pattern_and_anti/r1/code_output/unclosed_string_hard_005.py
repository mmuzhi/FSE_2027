from typing import List
import sys

class Solution:
    def componentValue(self, nums: List[int], edges: List[List[int]]) -> int:
        sys.setrecursionlimit(1000000)
        n = len(nums)
        tree = [[] for _ in range(n)]
        for u, v in edges:
            tree[u].append(v)
            tree[v].append(u)

        total = sum(nums)

        def can(target: int) -> bool:
            def dfs(u: int, p: int) -> int:
                ans = nums[u]
                for v in tree[u]:
                    if v != p:
                        ans += dfs(v, u)
                return 0 if ans == target else ans
            return dfs(0, -1) == 0

        divisors = []
        i = 1
        while i * i <= total:
            if total % i == 0:
                divisors.append(i)
                if i != total // i:
                    divisors.append(total // i)
            i += 1
        divisors.sort()

        for target in divisors:
            if target == total:
                return 0
            if can(target):
                return total // target - 1
        return 0