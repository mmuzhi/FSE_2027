#include <stdexcept>

class BankAccount {
public:
    BankAccount(int balance = 0) : balance(balance) {}

    // Deposits a certain amount into the account, increasing the account
    // balance, returns the current account balance.
    // Throws std::invalid_argument("Invalid amount") if amount is negative.
    int deposit(int amount) {
        if (amount < 0) {
            throw std::invalid_argument("Invalid amount");
        }
        balance += amount;
        return balance;
    }

    // Withdraws a certain amount from the account, decreasing the account
    // balance, returns the current account balance.
    // Throws std::invalid_argument("Invalid amount") if amount is negative.
    // Throws std::invalid_argument("Insufficient balance.") if the withdrawal
    // amount exceeds the account balance.
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

    // Returns the account balance.
    int view_balance() const {
        return balance;
    }

    // Transfers a certain amount from the current account to another account.
    // Withdraw is attempted first; if it throws, the deposit is not performed
    // (matching the Python control flow).
    void transfer(BankAccount& other_account, int amount) {
        withdraw(amount);
        other_account.deposit(amount);
    }

private:
    int balance;
};