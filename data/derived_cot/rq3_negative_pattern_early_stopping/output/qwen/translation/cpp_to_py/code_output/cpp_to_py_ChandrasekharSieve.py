class ChandrasekharSieve:
    def __init__(self, n):
        self.n = n
        self.primes = self._generate_primes()

    def _generate_primes(self):
        if self.n < 2:
            return []
        
        sieve = [True] * (self.n + 1)
        sieve[0] = sieve[1] = False
        
        p = 2
        while p * p <= self.n:
            if sieve[p]:
                for i in range(p * p, self.n + 1, p):
                    sieve[i] = False
            p += 1
        
        primes = [i for i, is_prime in enumerate(sieve) if is_prime]
        return primes

    def get_primes(self):
        return self.primes