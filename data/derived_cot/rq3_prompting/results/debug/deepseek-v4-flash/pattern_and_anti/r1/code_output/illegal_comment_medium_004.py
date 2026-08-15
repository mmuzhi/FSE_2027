from typing import List

class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        MOD = 10**9 + 7
        stack = []
        res = 0
        n = len(arr)

        for i, num in enumerate(arr):
            while stack and arr[stack[-1]] > num:
                cur = stack.pop()
                left = stack[-1] if stack else -1
                res += arr[cur] * (cur - left) * (i - cur)
            stack.append(i)

        while stack:
            cur = stack.pop()
            left = stack[-1] if stack else -1
            res += arr[cur] * (cur - left) * (n - cur)

        return res % MOD