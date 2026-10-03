class Solution:
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        # Create a memoization array of size n+1
        Fib = [-1] * (n+1)
        Fib[0] = 0
        Fib[1] = 1
        
        # Use recursion with memoization
        if Fib[n] != -1:
            return Fib[n]
        Fib[n] = self.fib(n-1) + self.fib(n-2)
        return Fib[n]