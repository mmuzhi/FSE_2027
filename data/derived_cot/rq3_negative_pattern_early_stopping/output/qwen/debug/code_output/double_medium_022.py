class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        n = len(arr)
        mod = 10**9 + 7
        left = [0] * n  # left[i] will be the index of the previous smaller element
        right = [n-1] * n  # right[i] will be the index of the next greater or equal element? Actually, we want the next smaller element for boundaries.

        # Compute left boundaries: the previous smaller element
        stack = []
        for i in range(n):
            while stack and arr[stack[-1]] > arr[i]:
                stack.pop()
            left[i] = stack[-1] if stack else -1
            stack.append(i)

        # Clear the stack for the right boundaries
        stack = []
        for i in range(n-1, -1, -1):
            while stack and arr[stack[-1]] >= arr[i]:
                stack.pop()
            right[i] = stack[-1] if stack else n
            stack.append(i)

        total = 0
        for i in range(n):
            total = (total + arr[i] * (i - left[i]) * (right[i] - i)) % mod

        return total