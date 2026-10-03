#include <vector>
#include <iostream>

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

        for (int p = 2; p * p <= n; ++p) {
            if (sieve[p]) {
                for (int i = p * p; i <= n; i += p) {
                    sieve[i] = false;
                }
            }
        }

        std::vector<int> primes;
        for (int i = 2; i <= n; ++i) {
            if (sieve[i]) {
                primes.push_back(i);
            }
        }

        return primes;
    }

public:
    ChandrasekharSieve(int n) : n(n), primes(generatePrimes()) {}

    std::vector<int> getPrimes() const {
        return primes;
    }
};

int main() {
    ChandrasekharSieve cs(20);
    for (int prime : cs.getPrimes()) {
        std::cout << prime << " ";
    }
    std::cout << std::endl;
    return 0;
}