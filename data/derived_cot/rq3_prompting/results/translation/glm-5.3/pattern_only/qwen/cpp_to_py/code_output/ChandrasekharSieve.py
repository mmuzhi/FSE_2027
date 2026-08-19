class ChandrasekharSieve:
    def __init__(self, n):
        self._n = n
        self._primes = self._generate_primes()

    def _generate_primes(self):
        if self._n < 2:
            return []

        sieve = [True] * (self._n + 1)
        sieve[0] = sieve[1] = False

        p = 2
        while p * p <= self._n:
            if sieve[p]:
                for i in range(p * p, self._n + 1, p):
                    sieve[i] = False
            p += 1

        return [i for i in range(2, self._n + 1) if sieve[i]]

    def get_primes(self):
        return self._primes.copy()