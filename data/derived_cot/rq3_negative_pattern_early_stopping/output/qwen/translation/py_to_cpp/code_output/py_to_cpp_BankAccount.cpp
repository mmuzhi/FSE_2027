#include <stdexcept>
#include <string>

class BankAccount {
public:
    BankAccount(int balance = 0) : balance(balance) {}

    int deposit(int amount) {
        if (amount < 0) {
            throw std::runtime_error("Invalid amount");
        }
        balance += amount;
        return balance;
    }

    int withdraw(int amount) {
        if (amount < 0) {
            throw std::runtime_error("Invalid amount");
        }
        if (amount > balance) {
            throw std::runtime_error("Insufficient balance.");
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

private:
    int balance;
};