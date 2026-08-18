class ChandrasekharSieve:
    def __init__(self, n):
        self.n = n
        self.primes = self._generate_primes()

    def _generate_primes(self):
        n = self.n
        if n < 2:
            return []

        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False

        p = 2
        while p * p <= n:
            if sieve[p]:
                for i in range(p * p, n + 1, p):
                    sieve[i] = False
            p += 1

        return [i for i in range(2, n + 1) if sieve[i]]

    def get_primes(self):
        return self.primes[:]