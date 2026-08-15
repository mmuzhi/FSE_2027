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
        sieve[0] = false;
        sieve[1] = false;

        int p = 2;
        while (p * p <= n) {
            if (sieve[p]) {
                for (int i = p * p; i <= n; i += p) {
                    sieve[i] = false;
                }
            }
            p += 1;
        }

        std::vector<int> primes;
        for (int i = 2; i <= n; i++) {
            if (sieve[i]) {
                primes.push_back(i);
            }
        }

        return primes;
    }

public:
    ChandrasekharSieve(int n) : n(n), primes(generatePrimes()) {}

    std::vector<int>& getPrimes() {
        return primes;
    }
};

int main() {
    ChandrasekharSieve cs(20);
    std::vector<int>& primes = cs.getPrimes();

    std::cout << "[";
    for (size_t i = 0; i < primes.size(); ++i) {
        if (i > 0) {
            std::cout << ", ";
        }
        std::cout << primes[i];
    }
    std::cout << "]" << std::endl;

    return 0;
}