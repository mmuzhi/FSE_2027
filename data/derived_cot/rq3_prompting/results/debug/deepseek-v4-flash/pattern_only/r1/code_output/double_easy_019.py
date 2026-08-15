class Solution:
    def fib(self, n: int) -> int:
        if n <= 1:
            return n

        memo = [-1] * (n + 1)
        memo[0] = 0
        memo[1] = 1

        def helper(k: int) -> int:
            if memo[k] != -1:
                return memo[k]
            memo[k] = helper(k - 1) + helper(k - 2)
            return memo[k]

        return helper(n)