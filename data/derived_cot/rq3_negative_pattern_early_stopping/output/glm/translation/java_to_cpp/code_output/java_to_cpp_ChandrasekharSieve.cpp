#include <iostream>
#include <vector>

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

        std::vector<int> primes;
        for (int i = 2; i <= n; i++) {
            if (sieve[i]) {
                primes.push_back(i);
            }
        }

        return primes;
    }

public:
    ChandrasekharSieve(int n) {
        this->n = n;
        this->primes = generatePrimes();
    }

    std::vector<int> getPrimes() {
        return primes;
    }
};

std::ostream& operator<<(std::ostream& os, const std::vector<int>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); ++i) {
        if (i != 0) {
            os << ", ";
        }
        os << v[i];
    }
    os << "]";
    return os;
}

int main() {
    ChandrasekharSieve cs(20);
    std::cout << cs.getPrimes() << std::endl;
    return 0;
}