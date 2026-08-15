from typing import List

class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        MOD = 10**9 + 7
        stack = []
        res = 0

        for i, num in enumerate(arr):
            while stack and arr[stack[-1]] > num:
                cur = stack.pop()
                left = stack[-1] if stack else -1
                right = i
                res += arr[cur] * (cur - left) * (right - cur)
            stack.append(i)

        while stack:
            cur = stack.pop()
            left = stack[-1] if stack else -1
            right = len(arr)
            res += arr[cur] * (cur - left) * (right - cur)

        return res % MOD