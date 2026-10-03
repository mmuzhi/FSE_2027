#include <vector>

class ChandrasekharSieve {
private:
    int n;
    std::vector<int> primes;

public:
    ChandrasekharSieve(int n) : n(n) {
        primes = generate_primes();
    }

    std::vector<int> generate_primes() {
        if (n < 2) {
            return {};
        }

        std::vector<bool> sieve(n + 1, true);
        sieve[0] = sieve[1] = false;

        int p = 2;
        while (static_cast<long long>(p) * p <= n) {
            if (sieve[p]) {
                for (int i = p * p; i <= n; i += p) {
                    sieve[i] = false;
                }
            }
            p += 1;
        }

        std::vector<int> result;
        for (int i = 2; i <= n; ++i) {
            if (sieve[i]) {
                result.push_back(i);
            }
        }

        return result;
    }

    std::vector<int> get_primes() {
        return primes;
    }
};