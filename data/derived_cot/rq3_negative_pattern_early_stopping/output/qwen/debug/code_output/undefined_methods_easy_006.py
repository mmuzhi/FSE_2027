class Solution:
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        Fib = [-1] * (n + 1)
        Fib[0] = 0
        Fib[1] = 1
        
        for i in range(2, n + 1):
            Fib[i] = Fib[i - 1] + Fib[i - 2]
        
        return Fib[n]