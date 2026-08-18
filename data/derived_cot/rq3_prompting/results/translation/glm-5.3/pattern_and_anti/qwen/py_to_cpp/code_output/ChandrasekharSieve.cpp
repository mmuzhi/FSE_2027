#include <vector>

class ChandrasekharSieve {
public:
    ChandrasekharSieve(int n) : n(n) {
        this->primes = this->generate_primes();
    }

    std::vector<int> generate_primes() {
        if (this->n < 2) {
            return {};
        }

        std::vector<bool> sieve(this->n + 1, true);
        sieve[0] = sieve[1] = false;

        int p = 2;
        while (p * p <= this->n) {
            if (sieve[p]) {
                for (int i = p * p; i <= this->n; i += p) {
                    sieve[i] = false;
                }
            }
            p += 1;
        }

        std::vector<int> primes;
        for (int i = 2; i <= this->n; i++) {
            if (sieve[i]) {
                primes.push_back(i);
            }
        }

        return primes;
    }

    std::vector<int> get_primes() {
        return this->primes;
    }

private:
    int n;
    std::vector<int> primes;
};