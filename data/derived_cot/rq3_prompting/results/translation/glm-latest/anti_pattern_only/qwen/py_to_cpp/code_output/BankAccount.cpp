#include <stdexcept>

class BankAccount {
public:
    long long balance;

    explicit BankAccount(long long balance = 0) : balance(balance) {}

    long long deposit(long long amount) {
        if (amount < 0) {
            throw std::invalid_argument("Invalid amount");
        }
        balance += amount;
        return balance;
    }

    long long withdraw(long long amount) {
        if (amount < 0) {
            throw std::invalid_argument("Invalid amount");
        }
        if (amount > balance) {
            throw std::invalid_argument("Insufficient balance.");
        }
        balance -= amount;
        return balance;
    }

    long long view_balance() const {
        return balance;
    }

    void transfer(BankAccount& other_account, long long amount) {
        withdraw(amount);
        other_account.deposit(amount);
    }
};