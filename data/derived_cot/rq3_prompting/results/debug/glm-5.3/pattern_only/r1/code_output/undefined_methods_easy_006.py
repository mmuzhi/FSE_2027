class Solution:
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        if n == 1:
            return 1
        Fib = [-1 for _ in range(n + 1)]
        Fib[0] = 0
        Fib[1] = 1
        return self._fib(n, Fib)

    def _fib(self, n, Fib):
        if Fib[n] != -1:
            return Fib[n]
        Fib[n] = self._fib(n - 1, Fib) + self._fib(n - 2, Fib)
        return Fib[n]