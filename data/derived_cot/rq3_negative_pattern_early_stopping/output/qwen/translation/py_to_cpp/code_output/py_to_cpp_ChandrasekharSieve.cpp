#include <vector>
#include <cmath>

class ChandrasekharSieve {
private:
    int n;
    std::vector<bool> sieve;
    std::vector<int> primes;

    void generate_primes() {
        if (n < 2) {
            primes.clear();
            return;
        }

        sieve.resize(n + 1, true);
        sieve[0] = sieve[1] = false;

        int p = 2;
        while (p * p <= n) {
            if (sieve[p]) {
                for (int i = p * p; i <= n; i += p) {
                    sieve[i] = false;
                }
            }
            p++;
        }

        primes.clear();
        for (int i = 2; i <= n; i++) {
            if (sieve[i]) {
                primes.push_back(i);
            }
        }
    }

public:
    ChandrasekharSieve(int n) : n(n), sieve(n + 1, true), primes() {
        sieve[0] = sieve[1] = false;
        generate_primes();
    }

    std::vector<int> get_primes() const {
        return primes;
    }
};