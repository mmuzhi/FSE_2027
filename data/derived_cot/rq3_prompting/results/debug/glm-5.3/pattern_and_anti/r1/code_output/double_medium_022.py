from typing import List

class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        MOD = 10**9 + 7
        stack = []
        res = 0
        n = len(arr)

        for i in range(n):
            while stack and arr[stack[-1]] > arr[i]:
                cur = stack.pop()
                left = stack[-1] if stack else -1
                res += arr[cur] * (i - cur) * (cur - left)
            stack.append(i)

        # Flush remaining elements whose next-smaller element is the end of array
        i = n
        while stack:
            cur = stack.pop()
            left = stack[-1] if stack else -1
            res += arr[cur] * (i - cur) * (cur - left)

        return res % MOD