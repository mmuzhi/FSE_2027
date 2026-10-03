#include <stdexcept>

class BankAccount {
private:
    int balance;

public:
    // Constructor with default balance of 0
    BankAccount(int balance = 0) : balance(balance) {}

    // Deposit: if amount is negative, throw; otherwise increase balance and return new balance
    int deposit(int amount) {
        if (amount < 0) {
            throw std::invalid_argument("Invalid amount");
        }
        balance += amount;
        return balance;
    }

    // Withdraw: if amount is negative or exceeds balance, throw; otherwise decrease balance and return new balance
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

    // View balance: return current balance
    int view_balance() const {
        return balance;
    }

    // Transfer: withdraw from this account, deposit to other account
    void transfer(BankAccount& other_account, int amount) {
        this->withdraw(amount);         // may throw
        other_account.deposit(amount);  // will only execute if withdraw succeeded
    }
};