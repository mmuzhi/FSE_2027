#include <iostream>
#include <vector>

class ChandrasekharSieve {
private:
    int n;
    std::vector<int> primes;

    std::vector<int> generatePrimes() {
        if (n < 2) {
            return {};
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

        std::vector<int> result;
        for (int i = 2; i <= n; i++) {
            if (sieve[i]) {
                result.push_back(i);
            }
        }

        return result;
    }

public:
    explicit ChandrasekharSieve(int n) : n(n), primes(generatePrimes()) {}

    const std::vector<int>& getPrimes() const {
        return primes;
    }
};

int main() {
    ChandrasekharSieve cs(20);
    const std::vector<int>& primes = cs.getPrimes();

    // Match Java's List.toString() format: [2, 3, 5, ...]
    std::cout << "[";
    for (std::size_t i = 0; i < primes.size(); ++i) {
        if (i > 0) {
            std::cout << ", ";
        }
        std::cout << primes[i];
    }
    std::cout << "]" << std::endl;

    return 0;
}