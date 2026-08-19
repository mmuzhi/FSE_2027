#include <vector>

class ChandrasekharSieve {
public:
    int n;
    std::vector<int> primes;

    explicit ChandrasekharSieve(int n) : n(n) {
        this->primes = generate_primes();
    }

    std::vector<int> generate_primes() {
        if (n < 2) {
            return {};
        }

        std::vector<bool> sieve(n + 1, true);
        sieve[0] = false;
        sieve[1] = false;

        for (int p = 2; static_cast<long long>(p) * p <= n; ++p) {
            if (sieve[p]) {
                for (int i = p * p; i <= n; i += p) {
                    sieve[i] = false;
                }
            }
        }

        std::vector<int> result;
        for (int i = 2; i <= n; ++i) {
            if (sieve[i]) {
                result.push_back(i);
            }
        }

        return result;
    }

    const std::vector<int>& get_primes() const {
        return primes;
    }
};