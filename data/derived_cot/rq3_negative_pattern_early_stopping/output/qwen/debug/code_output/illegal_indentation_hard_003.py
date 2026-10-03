class Solution:
    def maxNiceDivisors(self, primeFactors: int) -> int:
        if primeFactors == 1:
            return -1
        if primeFactors <= 3:
            return primeFactors
        
        a = 0
        temp = primeFactors
        while temp % 2 == 0:
            a += 1
            temp //= 2
        
        b = 0
        while temp % 3 == 0:
            b += 1
            temp //= 3
        
        d = (2 ** a) * (3 ** b)
        if d == 1:
            return -1
        
        return d