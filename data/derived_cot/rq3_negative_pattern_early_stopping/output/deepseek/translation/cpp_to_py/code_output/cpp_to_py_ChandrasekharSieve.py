class ChandrasekharSieve:
    """Sieve of Eratosthenes (named ChandrasekharSieve) generating primes up to n."""

    def __init__(self, n: int):
        self.n = n
        self.primes = self._generate_primes()

    def _generate_primes(self) -> list[int]:
        """Private method to compute primes up to self.n."""
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

        primes = [i for i in range(2, self.n + 1) if sieve[i]]
        return primes

    def get_primes(self) -> list[int]:
        """Return a copy of the list of primes."""
        return list(self.primes)