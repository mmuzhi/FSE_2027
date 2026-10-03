class ChandrasekharSieve:
    def __init__(self, n: int):
        self.n = n
        self.primes = self.generatePrimes()

    def generatePrimes(self):
        if self.n < 2:
            return []

        n = self.n
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False

        p = 2
        while p * p <= n:
            if sieve[p]:
                for i in range(p * p, n + 1, p):
                    sieve[i] = False
            p += 1

        primes = [i for i in range(2, n + 1) if sieve[i]]
        return primes

    def getPrimes(self):
        return self.primes


if __name__ == "__main__":
    cs = ChandrasekharSieve(20)
    print(cs.getPrimes())