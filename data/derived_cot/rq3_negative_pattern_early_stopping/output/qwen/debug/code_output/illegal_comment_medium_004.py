class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        n = len(arr)
        stack = []
        res = 0
        mod = 10**9 + 7
        
        # We'll compute the left boundaries (next smaller element to the left)
        left_bound = [-1] * n
        for i in range(n):
            while stack and arr[stack[-1]] > arr[i]:
                stack.pop()
            left_bound[i] = stack[-1] if stack else -1
            stack.append(i)
        
        # Clear the stack for the right boundaries
        stack = []
        right_bound = [n] * n
        for i in range(n-1, -1, -1):
            while stack and arr[stack[-1]] > arr[i]:
                stack.pop()
            right_bound[i] = stack[-1] if stack else n
            stack.append(i)
        
        # Now, for each element, compute the number of subarrays where it is the minimum
        for i in range(n):
            left_count = i - left_bound[i]   # number of elements to the left that are greater than arr[i]
            right_count = right_bound[i] - i  # number of elements to the right that are greater than arr[i]
            res = (res + arr[i] * left_count * right_count) % mod
        
        return res