class Solution:
    def fib(self, n: int) -> int:
        if n <= 1:
            return n

        Fib = [-1] * (n + 1)
        Fib[0] = 0
        Fib[1] = 1

        def helper(k: int) -> int:
            if Fib[k] != -1:
                return Fib[k]
            Fib[k] = helper(k - 1) + helper(k - 2)
            return Fib[k]

        return helper(n)