class ChandrasekharSieve:
    def __init__(self, n):
        self.n = n
        self.primes = self.generate_primes()

    def generate_primes(self):
        n = self.n
        if n < 2:
            return []

        sieve = [True] * (n + 1)
        sieve[0] = False
        sieve[1] = False

        p = 2
        while p * p <= n:
            if sieve[p]:
                for i in range(p * p, n + 1, p):
                    sieve[i] = False
            p += 1

        primes = []
        for i in range(2, n + 1):
            if sieve[i]:
                primes.append(i)

        return primes

    def get_primes(self):
        return self.primes


if __name__ == "__main__":
    cs = ChandrasekharSieve(20)
    print(cs.get_primes())