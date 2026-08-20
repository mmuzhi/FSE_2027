#include <cstddef>
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
        for (int i = 2; i <= n; ++i) {
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

// Prints a list in the same format as Java's List.toString(),
// as used by System.out.println(List).
static void printList(const std::vector<int>& list) {
    std::cout << '[';
    for (std::size_t i = 0; i < list.size(); ++i) {
        if (i > 0) {
            std::cout << ", ";
        }
        std::cout << list[i];
    }
    std::cout << ']' << std::endl;
}

int main() {
    ChandrasekharSieve cs(20);
    printList(cs.getPrimes());
    return 0;
}