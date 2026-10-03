#include <vector>
#include <cmath>

class ChandrasekharSieve {
private:
    int n;
    std::vector<int> primes;

    std::vector<int> generatePrimes() {
        if (n < 2) {
            return std::vector<int>();
        }

        std::vector<bool> sieve(n + 1, true);
        sieve[0] = sieve[1] = false;

        int p = 2;
        while (p * p <= n) {
            if (sieve[p]) {
                for (int i = p * p; i <= n; i += p) {
                    sieve[i] = false;
                }
            }
            p += 1;
        }

        std::vector<int> primesList;
        for (int i = 2; i <= n; i++) {
            if (sieve[i]) {
                primesList.push_back(i);
            }
        }
        return primesList;
    }

public:
    ChandrasekharSieve(int n) : n(n), primes(generatePrimes()) {}

    std::vector<int>& getPrimes() {
        return primes;
    }
};