class Solution:
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        if n == 1:
            return 1
        Fib = [-1 for _ in range(n + 1)]
        Fib[0] = 0
        Fib[1] = 1

        def compute(k: int) -> int:
            if Fib[k] != -1:
                return Fib[k]
            Fib[k] = compute(k - 1) + compute(k - 2)
            return Fib[k]

        return compute(n)