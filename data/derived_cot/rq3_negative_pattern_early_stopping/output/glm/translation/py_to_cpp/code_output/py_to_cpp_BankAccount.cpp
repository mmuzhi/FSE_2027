#include <stdexcept>

class BankAccount {
private:
    int balance;

public:
    BankAccount(int balance = 0) : balance(balance) {}

    int deposit(int amount) {
        if (amount < 0) {
            throw std::invalid_argument("Invalid amount");
        }
        balance += amount;
        return balance;
    }

    int withdraw(int amount) {
        if (amount < 0) {
            throw std::invalid_argument("Invalid amount");
        }
        if (amount > balance) {
            throw std::invalid_argument("Insufficient balance.");
        }
        balance -= amount;
        return balance;
    }

    int view_balance() const {
        return balance;
    }

    void transfer(BankAccount& other_account, int amount) {
        withdraw(amount);
        other_account.deposit(amount);
    }
};